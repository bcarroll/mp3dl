import logging
import subprocess as sp
from os import remove
from os.path import join as path_join
from os.path import isfile
from time import sleep

def convert_to_mp3(ffmpeg=None, inFile=None, outFile=None, bitrate='192k', codec="libmp3lame"):
    """
    Converts a input file to mp3
    command: ffmpeg -n -i inFile -acodec libmp3lame -ab 192k outFile
    """
    if ffmpeg is None:
        raise AttributeError("ffmpeg parameter is required")
        return "ERROR: ffmpeg parameter not specified"

    if inFile is None:
        raise AttributeError("inFile parameter is required")
        return "ERROR: inFile parameter not specified"

    if outFile is None:
        outFile = inFile

    if not outFile.lower().endswith(".mp3"):
        outFile = outFile + ".mp3"

    logging.debug("Waiting for download to complete before converting")
    for i in range(0,10):
        if isfile(inFile + '.temp'):
            sleep(1000)
    if isfile(inFile + '.temp'):
        logging.warn("Download does not appear to have completed successfully.  Temp file still exists...")
        inFile = inFile + '.temp'

    command = [ffmpeg,
                "-n",
                "-i", inFile,
                "-acodec", codec,
                "-ab", bitrate,
                outFile
                ]
    logging.debug(command)
    return _convert(command, inFile)

def _convert(command, inFile):
    """
    @param:
        command: command for conversion
    """
    logging.debug("Converting %s to MP3" % inFile)
    try:
        proc = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
        proc.wait()
        if proc.returncode:
            err = "\n".join(["Audio conversion: %s\n" % command,
            "WARNING: this command returned an error:", err.decode('utf8')])
            logging.error(err)
            raise IOError(err)
            return err
        del proc
    except IOError as e:
        logging.error('{0}'.format(e), exc_info=True)
        return '{0}'.format(e)
    try:
        logging.debug("Deleting downloaded file: %s" % inFile)
        remove(inFile)
    except Exception as e:
        logging.warn(e)