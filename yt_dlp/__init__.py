#!/usr/bin/env python3
# coding: utf-8

"""
yt-dlp: A feature-rich command-line audio/video downloader

Fork of yt-dlp with additional features and fixes.
"""

__license__ = 'Unlicense'
__version__ = '2024.01.01'

from .YoutubeDL import YoutubeDL
from .extractor import gen_extractors, list_extractors


def main(argv=None):
    """Main entry point for yt-dlp command line interface."""
    from .options import parseOpts
    from .utils import (
        DownloadError,
        ExistingVideoReached,
        MaxDownloadsReached,
        RejectedVideoReached,
        SameFileError,
        decodeOption,
        write_string,
    )
    import sys
    import traceback

    setproctitle = None
    try:
        from setproctitle import setproctitle
    except ImportError:
        pass

    if setproctitle:
        setproctitle('yt-dlp')

    try:
        parser, opts, args = parseOpts(argv)
    except SystemExit as e:
        sys.exit(e.code)

    # Set up the downloader
    ydl_opts = {
        'quiet': opts.quiet,
        'verbose': opts.verbose,
        'no_warnings': opts.no_warnings,
        'format': opts.format,
        'outtmpl': opts.outtmpl,
        'restrictfilenames': opts.restrictfilenames,
        'nooverwrites': opts.nooverwrites,
        'continuedl': opts.continue_dl,
        'noprogress': opts.noprogress,
        'playliststart': opts.playliststart,
        'playlistend': opts.playlistend,
        'noplaylist': opts.noplaylist,
        'playlistrandom': opts.playlist_random,
        'ignoreerrors': opts.ignoreerrors,
        'logtostderr': opts.outtmpl == '-',
        'writedescription': opts.writedescription,
        'writeinfojson': opts.writeinfojson,
        'writeannotations': opts.writeannotations,
        'writethumbnail': opts.writethumbnail,
        'write_all_thumbnails': opts.write_all_thumbnails,
        'writesubtitles': opts.writesubtitles,
        'writeautomaticsub': opts.writeautomaticsub,
        'allsubtitles': opts.allsubtitles,
        'listsubtitles': opts.listsubtitles,
        'subtitlesformat': opts.subtitlesformat,
        'subtitleslangs': opts.subtitleslangs,
        'matchtitle': decodeOption(opts.matchtitle),
        'rejecttitle': decodeOption(opts.rejecttitle),
        'max_downloads': opts.max_downloads,
        'prefer_free_formats': opts.prefer_free_formats,
        'trim_file_name': opts.trim_file_name,
        'verbose': opts.verbose,
        'dump_single_json': opts.dump_single_json,
        'simulate': opts.simulate,
        'skip_download': opts.skip_download,
        'callhome': opts.call_home,
        'external_downloader': opts.external_downloader,
        'external_downloader_args': opts.external_downloader_args,
        'postprocessors': [],
        'fixup': opts.fixup,
        'source_address': opts.source_address,
        'geo_bypass': opts.geo_bypass,
        'geo_bypass_country': opts.geo_bypass_country,
        'geo_bypass_ip_block': opts.geo_bypass_ip_block,
        'overwrites': opts.overwrites,
        'concurrent_fragment_downloads': opts.concurrent_fragment_downloads,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            retcode = ydl.download(args)
    except DownloadError:
        sys.exit(1)
    except SameFileError as e:
        write_string(f'ERROR: {e}\n', out=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        write_string('\n[yt-dlp] Interrupted by user\n', out=sys.stderr)
        sys.exit(1)
    except (MaxDownloadsReached, ExistingVideoReached, RejectedVideoReached):
        pass
    else:
        sys.exit(retcode)


if __name__ == '__main__':
    main()
