from astropy.coordinates import SkyCoord
from astropy import units as u

import csv, re

def get_sexadecimal_string(position):
    sexadecimal = "%02d%02d%02.0f" % position.ra.hms+re.sub(r"([+-])\d",r"\1","%+d%02d%02d%02.0f" % position.dec.signed_dms)
    return sexadecimal

def get_cutout_filename(position,size,survey,filter=None,extension=None):
    coords = get_sexadecimal_string(position)
    # note:the size as string already prints the units but remove space needed
    size   = str(size).replace(" ", "")#re.sub(r"\.?0+$","","%f" % size)
    filter = (lambda f: '' if f is None else f"-{f.name}")(filter)
    return f"{survey}_J{coords}_s{size}_{filter}{'.%s' % extension if not extension is None else ''}"

def extractCoordfromString(position, is_name=False):
    '''
    example accepted formats:
        > RA,DEC or RA DEC in degrees
        > '00h42m30s', '+41d12m00s' or 00h42m30s, +41d12m00s
        > '00 42 30 +41 12 00'
        > '00:42.5 +41:12'
    if is_name:
        > The name of the object to get coordinates for, e.g. 'M42'
    '''
    if is_name:
        return SkyCoord.from_name(position)
    # preformat string for consistency
    position = position.replace("'", "").replace(",", " ").replace("`", " ")
    if not ('h' in position or 'm' in position or ':' in position):
        # RA, DEC in degrees
        pos_list = [float(s) for s in re.findall(r'-?\d+\.?\d*', position)]
        if len(pos_list)==2: # if more than 2 it's an hour string
            return SkyCoord(pos_list[0], pos_list[1], unit=(u.deg, u.deg))

    return SkyCoord(position, unit=(u.hourangle, u.deg))

def readCoordsFromFile(csv_dictreader, max_batch=105):
    '''
    Takes a csv.DictReader object and parses coordinates from it
    Any columns matching RA, DEC header format are taken as coords
        if value nonempty
    secondarily if 'NAME' is in any headers then that value is evaluated
        as source name if value nonempty.
    '''
    # REMOVE SPACES, ALL CAPS, REMOVE BRACKETS, remove decimals, REMOVE 'J2000'
    potential_RA = ['RA', 'RIGHTASCENSION']
    potential_DEC = ['DEC', 'DECLINATION']

    positions = []
    headers = csv_dictreader.fieldnames
    name_h=ra_h=dec_h=None
    errors = []
    for h in headers:
        # REMOVE SPACES, ALL CAPS, REMOVE BRACKETS, remove decimals, REMOVE 'J2000'
        trimmed = re.sub(r" ?[.()\ \[\]]", "", h.upper().replace('J2000',''))
        print(trimmed)
        if "NAME" in trimmed and not name_h:
            name_h = h
        elif trimmed in potential_RA and not ra_h:
            ra_h = h
        elif trimmed in potential_DEC and not dec_h:
            dec_h = h
    if ra_h==None or dec_h==None and name_h==None:
        raise Exception('invalid headers for coordinates or name in .CSV!')

    succ_count = 0
    line_num = 1
    for line in csv_dictreader:
        if succ_count>=max_batch:
            errors.append("max batch size is {} locations, rest were skipped".format(max_batch))
            break
        to_get = None
        is_name = False
        curr_name = ""
        # prioritize ra/dec over name but still call "input" the name for table
        if ra_h and dec_h:
            if line[ra_h]!='' and line[dec_h]!='':
                to_get = line[ra_h] +' '+ line[dec_h]
                curr_name = to_get
        if name_h:
            if line[name_h]!='':
                curr_name = line[name_h]
                if not to_get:
                    to_get = line[name_h]
                    is_name = True
        if to_get:
            try:
                # use coords for location query but report "name" as name entered no matter what for user to see
                positions.append({"name": curr_name, "position": extractCoordfromString(to_get, is_name)})
                succ_count+=1
            except Exception as e:
                errors.append(str(e))
        line_num += 1
    return positions, errors