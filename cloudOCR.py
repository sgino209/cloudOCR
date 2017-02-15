# !/usr/bin/python
#   ___   ____ ____                           ____ _                 _
#  / _ \ / ___|  _ \    _____   _____ _ __   / ___| | ___  _   _  __| |  A generic OCR over cloud
# | | | | |   | |_) |  / _ \ \ / / _ \ '__| | |   | |/ _ \| | | |/ _` |  environment, may be used
# | |_| | |___|  _ <  | (_) \ V /  __/ |    | |___| | (_) | |_| | (_| |  as a reference code for
#  \___/ \____|_| \_\  \___/ \_/ \___|_|     \____|_|\___/ \__,_|\__,_|  using ABBYY and Microsoft API
#
# (c) Shahar Gino, Feb-2017, sgino209@gmail.com

from main_microsoft import main_microsoft
from main_abbyy import main_abbyy
from os import listdir, path, makedirs
from sys import exit, argv
from time import time
import getopt

# Python structuring way:
class Struct:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

# ---------------------------------------------------------------------------------------------------------------
def usage():
    print 'cloudOCR.py -f [img_file] -d [img_folder] -u [img_url] -x [ABBYY/Microsoft]'
    print 'Optional flags: --abbyy_appid, --abbyy_pwd, --microsoft_key, --result_path'

# ---------------------------------------------------------------------------------------------------------------
def main(_argv):

    # Default parameters:
    args = Struct(
        img_type = "URL",
        img_path = "https://www.lesrhabilleurs.com/wp-content/uploads/2016/03/Bell-Ross-BRS-Auto-Black-Officier-caseback.jpg",
        img_dir = "",
        sdk_type = "Microsoft",
        res_path = "output_results",
        abbyy_appid = "OCR_NaturalPhotos",
        abbyy_pwd = "nTFgj52alg/l+btAO2YQ4rdr",
        microsoft_key = "5f9380fe82404c40bb7cc96cf7961168"
        # microsoft_key = "0367fddb014b460b8b54c23c94ef53ed"
        )

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    # User-Arguments parameters (overrides Defaults):
    try:
        opts, user_args = getopt.getopt(_argv, "hf:d:u:x:", ["abbyy_appid=", "abbyy_pwd=", "microsoft_key=", "result_path="])

        for opt, user_arg in opts:
            if opt == '-h':
                usage()
                exit()
            elif opt in "-f":
                args.img_type = "FILE"
                args.img_path = user_arg
            elif opt in "-d":
                args.img_type = "DIR"
                args.img_dir = user_arg
            elif opt in "-u":
                args.img_type = "URL"
                args.img_path = user_arg
            elif opt in "-x":
                args.sdk_type = user_arg
            elif opt in "--abbyy_appid":
                args.abbyy_appid = user_arg
            elif opt in "--abbyy_pwd":
                args.abbyy_pwd = user_arg
            elif opt in "--microsoft_key":
                args.microsoft_key = user_arg
            elif opt in "--result_path":
                args.res_path = user_arg

    except getopt.GetoptError:
        usage()
        exit(2)

    if args.sdk_type not in ['ABBYY', 'Microsoft']:
        usage()
        exit(2)

    # -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- .. -- ..
    # Call for sub-main engines:
    predictions = {}
    f = None

    if not path.exists(args.res_path):
        makedirs(args.res_path)

    if args.img_type == 'DIR':
        sources_pre = listdir(args.img_dir)
        sources = []
        for filename in sources_pre:
            sources.append(path.join(args.img_dir, filename))
        f = open(path.join(args.res_path, args.sdk_type.lower()) + '.summary.txt', 'w')
        args.img_type = 'FILE'

    else:
        sources = [args.img_path]

    for filename in sources:
        print('Analyzing: %s' % filename)
        args.img_path = filename

        # Bernoulli Naive Bayes:
        if args.sdk_type == "ABBYY":
            predictions[filename] = main_abbyy(args)

        # K-Nearest Neighbors (k=5):
        elif args.sdk_type == "Microsoft":
            predictions[filename] = main_microsoft(args)

        # Print results:
        print predictions[filename]
        if f:
            f.write(filename + ' ---> ' + str(len(predictions[filename])) + ' characters\n')

    if f:
        f.close()

# ---------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    t0 = time()
    print 'Start'

    main(argv[1:])

    t1 = time()
    t_elapsed_sec = t1 - t0
    print('Done! (%.2f sec)' % t_elapsed_sec)
