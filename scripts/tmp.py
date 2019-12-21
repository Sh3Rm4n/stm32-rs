import yaml
import fnmatch
import os.path
import glob

import svdpatch


# print(peripheral_old[0])
# peripheral_list = list(peripheral_new)[0]
# key_new = []
# key_old = []
# for key in peripheral_new.keys():
#     print(key)
#     print(svdpatch.spec_ind(key))
#     key_new.append(key)
# for key in peripheral_old.keys():
#     print(key)
#     print(svdpatch.spec_ind(key))
#     key_old.append(key)
# print(key_new)
# print(key_old)
# print(list(peripheral_new.keys())[0])
# for key_new in peripheral_new.keys():
# matches = fnmatch.filter(list(peripheral_new.keys())[0], list(peripheral_old.keys())[0])
# print(matches)
# print(peripheral_list)
# print(type(peripheral_list))
# print(peripheral_new)


def check_matches(peripheral_old, peripheral_new):
    # TODO we have to consider `_include:`
    try:
        peripheral_old_keys = peripheral_old.keys()
    except (TypeError, AttributeError):
        return
    else:
        for key_old in peripheral_old_keys:
            # print(key_new)
            try:
                peripheral_new_keys = peripheral_new.keys()
            except AttributeError:
                break
            else:
                # FIXME:
                # new keys: ['MODER', 'OTYPER', 'OSPEEDR', 'PUPDR', 'IDR', 'ODR', 'BSRR', 'LCKR', 'AFR[LH]']
                # AFR[LH] matches []
                # Does not match anymore!
                # FIX: peripheral_new_keys is not interpreted as glob pattern and has to be interpreted as such
                # expand glob pattern if bracket sequence
                # now we could need the svd thing???
                matches = fnmatch.filter(list(peripheral_new_keys), key_old)
                print("old key:  {}".format(key_old))
                print("new keys: {}".format(list(peripheral_new_keys)))
                print("{} matches {}".format(key_old, matches))
                if not matches:
                    print("Does not match anymore!")
                    break
                # print(peripheral_new['GPIO[AH]'])
                # Go recursive
                for match in matches:
                    check_matches(peripheral_new[match], peripheral_old[key_old])

# TODO type annotation list[str]
def expand_glob(glob: list) -> list:
    # Loop over input list and generate an new list, with expanded libraries,
    # to not depend on a mutable state, as the parsed list is only used for comparison,
    # and the original data structure does'nt have to be mutated.
    # Do the same as, but ignore * as this wont be expanded
    # spec_ind can give us the position. Reuse it!

    # do not forget this case ASD[12340987]*
    # -> so do not ignore cases were a glob is there
    # or that one asdf1[1234980756]
    # ? expands to abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890
    expanded = []
    # li, ri = svdpatch.spec_ind(glob)
    if glob.find("*"):
        return glob
    else:
        question_mark_index = glob.find("?") # Assign find
        print(question_mark_index)
        if question_mark_index:
            print('yello')
        elif glob.find("]"):
            # replace list ? Entry with list a
            # append A-Z and 0-9
            return list
        elif glob.find("["):
            # find out number of entries between braces
            # create list of entries
            # loop of entries
                # replace braces with entries with list[i]
                # remove brace entry in list
                # append orig list with new generated entry
            pass
    # Nothing to expand
    return glob

def main():
    with open("peripherals/gpio/gpio_v2.yaml", encoding='utf-8') as f:
        peripheral_old = yaml.safe_load(f)
    # with open("peripherals/gpio/gpio_f373_f3x8.yaml", encoding='utf-8') as f:
    #     peripheral_new = yaml.safe_load(f)
    # check_matches(peripheral_old, peripheral_new)
    test = ["GLOB?"]
    expand_glob(test)


if __name__ == "__main__":
    main()
