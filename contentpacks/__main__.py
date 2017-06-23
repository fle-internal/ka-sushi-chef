"""
makepack

Usage:
  makecontentpacks ka-lite <lang> <version> [options]
  makecontentpacks -h | --help
  makecontentpacks --version

--subtitlelang=subtitle-lang   The language to download subtitles in.
--contentlang=content-lang     The language to for content, i.e. what language to pull from Khan Academy.
--interfacelang=interface-lang The language to pull from CrowdIn for KALite's/Kolibri's interface.
--videolang=video-lang         The language of dubbed videos, i.e. what dubbed video mapping language to use.
--out=outdir                   The path to place the final content pack.
--logging=log_file             The file for logging output. Defaults to stderr if not specified.
--no-subtitles                 If specified, will omit downloading and including any subtitles.
--no-assessment-items          If specified, will omit downloading and including any assessment item data.
--no-assessment-resources      If specified, will omit downloading and including any resources (images, json files) needed to render assessment item exercises.
--no-dubbed-videos             If specified, will omit including dubbed video mappings

"""
from docopt import docopt
from pathlib import Path
from contentpacks.khanacademy import retrieve_language_resources, apply_dubbed_video_map, \
    retrieve_all_assessment_item_data
from contentpacks.utils import translate_nodes, remove_untranslated_exercises, \
    remove_assessment_data_with_empty_widgets, remove_nonexistent_assessment_items_from_exercises, \
    clean_node_data_items

import logging
import pickle


def make_language_pack(lang, version, sublangargs, filename, ka_domain, no_assessment_items, no_subtitles, no_assessment_resources, no_dubbed_videos):
    node_data, subtitle_data, content_catalog = retrieve_language_resources(version, sublangargs, ka_domain, no_subtitles, no_dubbed_videos)

    node_data = translate_nodes(node_data, content_catalog)
    node_data = list(node_data)
    node_data, dubbed_video_count = apply_dubbed_video_map(node_data, subtitle_data, sublangargs["video_lang"])

    # now include only the assessment item resources that we need
    all_assessment_data, all_assessment_files = retrieve_all_assessment_item_data(
        no_item_data=no_assessment_items,
        no_item_resources=no_assessment_resources,
        node_data=node_data,
        lang=lang,
        content_catalog=content_catalog,
    )
    all_assessment_data = list(remove_assessment_data_with_empty_widgets(all_assessment_data))
    node_data = remove_nonexistent_assessment_items_from_exercises(node_data, all_assessment_data)

    node_data = clean_node_data_items(node_data)
    node_data = remove_untranslated_exercises(node_data, all_assessment_data) if lang != "en" else node_data
    node_data = list(node_data)
    node_data = sorted(node_data, key=lambda x: x.get('sort_order'))

    with open('node_data_{0}.pickle'.format(lang), 'wb') as handle:
        pickle.dump(node_data, handle)

    with open('assessment_data_{0}.pickle'.format(lang), 'wb') as handle:
        pickle.dump(all_assessment_data, handle)


def normalize_sublang_args(args):
    """
    Transform the command line arguments we have into something that conforms to the retrieve_language_resources interface.
    This mostly means using the given lang parameter as the default lang, overridable by the different sublang args.
    """
    return {
        "video_lang": args['--videolang'] or args['<lang>'],
        "content_lang": args['--contentlang'] or args['<lang>'],
        "interface_lang": args['--interfacelang'] or args['<lang>'],
        "subtitle_lang": args['--subtitlelang'] or args['<lang>'],
    }


def main():
    import os
    args = docopt(__doc__)

    assert args["ka-lite"], ("Sorry, content packs for non-KA Lite "
                             "software aren't implemented yet.")
    del args["ka-lite"]

    lang = args["<lang>"]
    version = args["<version>"]
    out = Path(args["--out"]) if args['--out'] else Path.cwd() / "{lang}.zip".format(lang=lang)

    ka_domain = os.environ.get("KA_DOMAIN") or "www.khanacademy.org"

    sublangs = normalize_sublang_args(args)

    no_assessment_items = args["--no-assessment-items"]
    no_assessment_resources = args['--no-assessment-resources']
    no_subtitles = args['--no-subtitles']
    no_dubbed_videos = args['--no-dubbed-videos']

    # log_file = args["--logging"] or "debug.log"

    logging.basicConfig(level=logging.INFO)

    try:
        make_language_pack(lang, version, sublangs, out, ka_domain, no_assessment_items, no_subtitles, no_assessment_resources, no_dubbed_videos)
    except Exception as e:           # This is allowed, since we want to potentially debug all errors
        import os
        if not os.environ.get("DEBUG"):
            raise
        else:
            logging.error("An exception occured! {}".format(e))
            import pdb
            pdb.post_mortem()
            # raise


if __name__ == "__main__":
    main()
