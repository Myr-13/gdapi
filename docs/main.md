# Local levels reading
Steps for get readable xml data of all levels:
- Xor decrypt with key 11
- Replace '-' to '+' and replace '_' to '/'
- Decrypt replaced string with base64
- Unpack this with gzip


# Reading level data from xml
- Replace '-' to '+' and replace '_' to '/'
- Decrypt replaced string with base64
- Unpack this with gzip


# Entities
Entity object is a sequence of attributes

Format of attributes data: `attr1,value1,attr2,value2,attr3,value3`

Check `gdapi/entity.py` for get attributes id's

Check `docs/entitites_id.txt` for get useful id's of entities


# Color channels
Groups packing format is like entities, but separator is '_'

Format: `attr1_value1_attr2_value2_attr3_value3`

Check `gdapi/color_channel.py` for get attributes id's


# HSV packing
Format: `HaSaBa1a2`

hue(int) + 'a' + saturation(float/int) + 'a' + brightness(float/int) + 'a' + 1st_checkbox(int) + 'a' + 2st_checkbox(int)


# Groups packing
Format: `group1.group2.group3.group4`
