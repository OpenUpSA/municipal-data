from __future__ import absolute_import

import codecs

import scss

from django.conf import settings

from whitenoise.storage import CompressedManifestStaticFilesStorage
from pipeline.storage import PipelineMixin
from pipeline.compilers import SubProcessCompiler


class GzipManifestPipelineStorage(PipelineMixin, CompressedManifestStaticFilesStorage):
    manifest_strict = False

    # Silence errors from vega-lite missing some map tiles
    def post_process(self, paths, dry_run=False, **options):
        for result in super().post_process(paths, dry_run=dry_run, **options):
            name, hashed_name, processed = result
            if isinstance(processed, Exception) and '.map' in str(processed):
                yield name, hashed_name, True
            else:
                yield result


class PyScssCompiler(SubProcessCompiler):
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.scss')

    def compile_file(self, infile, outfile, outdated=False, force=False):
        if not outdated and not force:
            return

        result = scss.compiler.compile_file(
            infile,
            search_path=settings.PYSCSS_LOAD_PATHS)

        with codecs.open(outfile, 'w', encoding='utf-8') as f:
            f.write(result)
