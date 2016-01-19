import os
import re
import sys
import ConfigParser as cp


class MyConfigParser(cp.SafeConfigParser):
    def __init__(self):
        cp.RawConfigParser.__init__(self)

    def optionxform(self, str):
        return str

    def add_section(self, section, items=None):
        if items:
            if not self.has_section(section):
                self.add_section(section)
            for item in items:
                self.add(section, item[0], item[1])
        else:
            try:
                cp.RawConfigParser.add_section(self, section)
            except cp.DuplicateSectionError, ex:
                return

    def set_section(self, section, items=None):
        if items:
            if not self.has_section(section):
                self.add_section(section)
            for item in items:
                self.set(section, item[0], item[1])
        else:
            self.add_section(section)

    def get_section(self, section):
        var = {}
        for item in self.items(section):
            var[item[0]] = item[1]
        return var

    def add(self, section, name=None, value=None):
        if name:
            if self.has_option(section, name) and self.get(section, name) is not None:
                return
            else:
                self.set(section, name, value)
        else:
            self.add_section(section)

    def set(self, section, name=None, value=None):
        if name:
            try:
                cp.RawConfigParser.set(self, section, name, value)
            except cp.NoSectionError, ex:
                self.add_section(section)
                cp.RawConfigParser.set(self, section, name, value)
        else:
            self.add_sectioin(section)

    def rename(self, old, new):
        try:
            self.set_section(new, self.items(old))
        except cp.NoSectionError, ex:
            return False
        self.remove_section(old)

    def write(self, fp):
        try:
            cp.SafeConfigParser.write(self, fp)
        except cp.InterpolationMissingOptionError, ex:
            cp.RawConfigParser.write(self, fp)


class Work(object):
    def __init__(self, default_config):
        self.config = MyConfigParser()
        self.commands = []
        self.default_config = self.__read_config(default_config)

    def __del__(self):
        try:
            self.write_config(self.config.get('outfiles', 'config'))
            self.write_shell(self.config.get('outfiles', 'shell'))
        except cp.NoSectionError, ex:
            pass

    @staticmethod
    def __read_config(config):
        if config.__class__ == str:
            cfg = MyConfigParser()
            cfg.readfp(open(config))
            config = cfg
        return config

    def set_params(self, config, section_name='params', vars=None):
        params_list = self.default_config.options(section_name)
        config = self.__read_config(config)
        self.load_default_section(section_name)
        if config is None:
            return None
        try:
            param_dict = config.get_section(section_name)
        except cp.NoSectionError, ex:
            return None
        for option in params_list:
            try:
                self.config.set(section_name, option, param_dict[option])
            except KeyError, ex:
                if self.config.get(section_name, str(ex).strip("'")) is None:
                    raise KeyError, ex
        if vars is not None:
            for option, value in vars.iteritems():
                self.config.set(section_name, option, value)

    def set_config(self, config):
        config = self.__read_config(config)
        if config is None:
            return None
        for section in config.sections():
            self.config.set_section(section, items=config.items(section, raw=True))

    def load_default_section(self, section):
        _vars = None
        while 1:
            try:
                self.config.add_section(section, items=self.default_config.items(section, vars=_vars))
            except cp.InterpolationMissingOptionError, ex:
                if _vars is None:
                    _vars = {}
                _vars[ex.reference] = self.config.get('params', ex.reference)
            else:
                break
        if _vars is None:
            return
        for option in _vars.iterkeys():
            self.config.remove_option(section, option)

    def load_default_config(self):
        config = self.default_config
        if config is None or not config.sections():
            return None
        for section in config.sections():
            self.load_default_section(section)

    def write_config(self, out_file):
        out_dir = os.path.dirname(out_file)
        if not os.path.exists(out_dir):
            os.system('mkdir -p %s' % out_dir)
        fp = open(out_file, 'w')
        self.config.write(fp)
        fp.close()

    def write_shell(self, shell_file):
        if not os.path.exists(os.path.dirname(shell_file)):
            os.system('mkdir -p %s' % os.path.dirname(shell_file))
        shell = open(shell_file, 'w')
        #        shell.write("echo -e 'Begin at : \c' && date\n")
        for cmd in self.commands:
            shell.write(cmd + '\n')
        # shell.write(cmd + " && echo -e 'This-Work-is-Completed! : \c' && date\n")
        #        shell.write("echo -e 'All target finished at : \c' && date\n")
        shell.close()


class GroupFileError():
    def __init__(self, group_file):
        self.group_file = group_file

    def __str__(self):
        message = "the groupfile %s must in two cols!\n" % self.group_file
        return message


class AlphaGroupFileError(GroupFileError):
    def __str__(self):
        message = "the alpha group file %s must contain all samples!\n" % self.group_file
        return message


class UserConfigChecker(object):
    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        if exception_type is None:
            pass
        elif exception_type == KeyError:
            sys.stderr.write('the config %s is missing!\n' % exception_val)
            #  sys.exit()
        elif exception_type == AssertionError:
            sys.stderr.write('the config setting is error:\n\t%s\n' % exception_val)
            #  sys.exit()
        elif exception_type == ValueError:
            sys.stderr.write('the config setting is error:\n\t%s\n' % exception_val)
            #  sys.exit()
        elif exception_type == cp.InterpolationMissingOptionError:
            key = re.search('key\s+:\s+(.+)\n', str(exception_val)).group(1)
            sys.stderr.write('the config %s can not find!\n' % key)
            #  sys.exit()
        elif exception_type == GroupFileError:
            sys.stderr.write(str(exception_val))
            sys.stderr.write('please set the group_file correct!\n')
            #  sys.exit()
        elif exception_type == AlphaGroupFileError:
            sys.stderr.write(str(exception_val))
            sys.stderr.write('please set the alpha_group_file correct!\n')
            # sys.exit()
        else:
            sys.stderr.write('%s : %s' % (exception_type, exception_val))
            #  sys.exit()


class Pipeline(Work):
    def __init__(self, config):
        super(Pipeline, self).__init__(config)
        self.set_config(config)
        try:
            self.job_id = self.config.get('params', 'job_id')
        except cp.NoOptionError:
            self.job_id = 'S'
        try:
            self.check_config()
        except:
            sys.stderr.write('config file check failed\n')
        self.html_hold_jobs = []

    def check_config(self):
        with UserConfigChecker():
            params = self.config.get_section('params')
            params['job_id']
            assert params['data_type'] == '16S' or params['data_type'] == 'ITS', 'data_type : %s' % params['data_type']
            assert os.path.isdir(params['work_dir']), 'work_dir : %s' % params['work_dir']
            assert os.path.isfile(params['name_list']), 'name_list : %s' % params['name_list']
            sample_num = os.popen("awk '{print $2}' %s| sort -u|wc -l" % params['name_list']).read().rstrip()
            for file in re.split('\s+', params['group_files']):
                assert os.path.isfile(file), 'group_files : %s' % file
                if not self.check_group_file(file):
                    raise GroupFileError, file
            assert os.path.isfile(params['alpha_group_file']), 'alpha_group_file : %s' % params['alpha_group_file']
            if not self.check_group_file(params['alpha_group_file']):
                raise GroupFileError, params['alpha_group_file']
            if os.popen("awk '{print $1}' %s|sort -u|wc -l" % params['alpha_group_file']).read().rstrip() != sample_num:
                raise AlphaGroupFileError, params['alpha_group_file']
            assert os.path.isdir(params['raw_data_dir']), 'raw_data_dir : %s' % params['raw_data_dir']
            for file in re.split('\s', params['fq_for_merge']):
                assert os.path.isfile(file), 'fq_for_merge : %s' % file
            params['require'] = int(params['require'])
            assert os.path.isdir(os.path.dirname(params['pipeline_shell'])), 'pipeline_shell : %s directory not exist' % \
                                                                             params['pipeline_shell']

    def check_group_file(self, group_file):
        if os.popen('file %s' % group_file).read().strip().split(': ')[-1] == 'empty':
            return False
        count = 0
        with open(group_file) as fp:
            for line in fp:
                count += 1
                tabs = line.split('\t')
                if len(tabs) != 2:
                    return False
        return True

    @staticmethod
    def make_shell(work_shell, work_list):
        from settings import FUNCTIONAL_SCRIPT_DIR
        if not os.path.isdir(os.path.dirname(work_shell)):
            os.system('mkdir -p %s' % os.path.dirname(work_shell))
        work_shell = open(work_shell, 'w')
        for (work, config) in work_list:
            script = '%s/%s.py' % (FUNCTIONAL_SCRIPT_DIR, work)
            work_shell.write('python %s %s\n' % (script, config))
        work_shell.close()

    @staticmethod
    def merge_shell(total_shell, shell_list):
        total_shell = open(total_shell, 'w')
        for shell in shell_list:
            total_shell.write('sh %s\n' % shell)
        total_shell.close()

    def check_file(self, file):
        if not os.path.isfile(file):
            return False
        with open(file) as fp:
            try:
                fp.next()
            except  StopIteration:
                return False
        return True

    def add_job(self, job_name, shell, prep=None, vf='5G', queue='all.q'):
        if not self.check_file(shell):
            return None
        self.html_hold_jobs.append(job_name)
        qsub_name = '%s_%s' % (self.job_id, job_name)
        __o_file = '%s.o' % shell
        __e_file = '%s.e' % shell
        if os.path.isfile(__o_file):
            os.remove(__o_file)
        if os.path.isfile(__e_file):
            os.remove(__e_file)
        job_name_satisfied = re.sub('\W', '_', job_name)
        cmd = '%s=`qsub -cwd -l vf=%s -q %s -N %s -e %s -o %s -terse' % (job_name_satisfied, vf, queue, qsub_name,
                                                                         __e_file, __o_file)
        if prep is not None:
            if prep.__class__ == list:
                prep_satisfied = map(lambda s: re.sub('\W', '_', s), prep)
                cmd += ' -hold_jid %s' % ','.join(map(lambda s: '$' + s, prep_satisfied))
            else:
                prep_satisfied = re.sub('\W', '_', prep)
                cmd += ' -hold_jid $%s' % prep_satisfied
        cmd += ' %s`' % shell
        self.commands.append(cmd)

    def __del__(self):
        self.write_shell(self.config.get('params', 'pipeline_shell'))


class SubWork(Work):
    def __init__(self, work_id, cfg_in):
        if cfg_in.__class__ == str:
            cfg = MyConfigParser()
            cfg.readfp(open(cfg_in))
            cfg_in = cfg
        super(SubWork, self).__init__()
        self.work_id = work_id
        cfg_in.set(work_id, 'work_dir', cfg_in.get('all', 'work_dir'))
        self.config = cfg_in
