/**
 * Created by rnaude on 24/03/14.
 */
module.exports = function (grunt) {
    grunt.initConfig({
        connect: {
            server: {
                options: {
                    base: "",
                    port: 9999
                }
            }
        },
        watch: {},
        webdriver: {
            options: {
                desiredCapabilities: {
                    browserName: 'chrome'
                }
            },
            sometests: {
                tests: ['smoketest/backupPower.py']
            }
        }
    });

    // loading dependencies
    for (var key in grunt.file.readJSON("package.json").devDependencies) {
        if (key !== "grunt" && key.indexOf("grunt") === 0) {
            grunt.loadNpmTasks(key);
        }
    }

//    grunt.registerTask("dev", ["connect", "watch"]);
    grunt.registerTask("default", ["webdriver:sometests"]);
};