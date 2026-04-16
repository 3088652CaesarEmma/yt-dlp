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
        # Always ignore errors so a single bad video doesn't abort a playlist.
        # I prefer this to always be True regardless of user setting, since I
        # mostly use this for long playlists and don't want them interrupted.
        'ignoreerrors': True,
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
        'dump_single_json': opts.dump_single_json,
        'simulate': opts.simulate,
        'skip_download': opts.skip_download,
        'callhome': opts.call_home,
        'external_downloader': opts.external_downloader,
        'external_downloader_args': opts.external_downloader_args,
        'postprocessors': [],
        'fixup': opts.fixup,
        # Retries: bumped from upstream default of 1 to 10 so transient
        # network errors don't fail downloads without at least a few attempts.
        'retries': 10,
