import os
import re

def _absolute_path(value, prefix=None):
    if os.path.isabs(value):
        return value
    if prefix is None:
        return os.path.abspath(value)
    if isinstance(prefix, list):
        prefix.append(value)
        return os.path.join(*prefix)
    return os.path.join(prefix, value)

def _filter_variant(value):
    variant = re.compile('([ +~][^ %+~@]+)*([ ^%][^ ^%]+)*')
    if isinstance(value, str):
        return variant.sub("", value).strip()
    return [ variant.sub("", v).strip() for v in value ]

def _version(value):
    filtered_value = _filter_variant(value)
    version_re = re.compile(r"@([^+~\^@]+)")
    match = version_re.search(filtered_value)
    if match:
        logger.debug("Found version \'{}\' for {}".format(
            match.group(1), filtered_value))
        return match.group(1)
    return None

def _regex_replace(s, find, replace):
    """A non-optimal implementation of a regex filter"""
    ns = re.sub(find, replace, s)
    return ns

def _cuda_variant(environment, arch=True,
                  extra_off='', extra_on='',
                  stack='stable',
                  dep=False):
    if 'gpu' not in environment or environment['gpu'] != 'nvidia':
        return '~cuda{}'.format(extra_off)

    variant = "+cuda"
    if arch:
        variant = '{0} cuda_arch={1}'.format(
            variant,
            environment[stack]['cuda']['arch'].replace('sm_', '')
        )
        variant = "{0} {1}".format(variant, extra_on)
    if dep:
        variant = '{0} ^{1}'.format(
            variant,
            environment[stack]['cuda']['package'])

    return variant

def _hip_variant(environment, arch=True,
                  extra_off='', extra_on='',
                  stack='stable',
                  dep=False):
    if 'gpu' not in environment or environment['gpu'] != 'amd':
        return '~hip{}'.format(extra_off)

    variant = '+hip{}'.format(extra_on)
    if arch:
        variant = '{0} amd_gpu_arch={1}'.format(
            variant,
            environment[stack]['rocm']['arch']
        )

    return variant

def _filter_compiler_name(value):
    def _filter_name(value):
        if 'llvm' in value:
            return value.replace('llvm', 'clang')
        if 'intel-oneapi-compilers' in value:
            return value.replace('intel-oneapi-compilers', 'oneapi')
        return value

    if isinstance(value, list):
        return [ _filter_name(entry) for entry in value ]
    return _filter_name(value)
