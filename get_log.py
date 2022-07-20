import os


def loc_get(project_path):
    android_base_version_list = 'android-12.0.0_r8	android-12.0.0_r9	android-12.0.0_r10	android-12.0.0_r11	android-12.0.0_r12	android-12.0.0_r13	android-12.0.0_r14	android-12.0.0_r15	android-12.0.0_r16	android-12.0.0_r17	android-12.0.0_r18	android-12.0.0_r19	android-12.0.0_r20	android-12.0.0_r21	android-12.0.0_r22'.split(
            "	")

    for version in android_base_version_list:
        os.chdir(project_path)
        os.system('git checkout ' + version)
        mc_dir = project_path + '//mc// '+ version
        git_log_file = mc_dir + "//gitlog"
        cmd = "git log --numstat --date=iso > " + git_log_file
        os.system(cmd)


if __name__ == '__main__':
    loc_get(r'D:\codes\aosp\android\base')