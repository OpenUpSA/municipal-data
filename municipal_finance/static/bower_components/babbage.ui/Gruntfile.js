module.exports = function(grunt) {
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-connect');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-html2js');
  grunt.loadNpmTasks('grunt-aws-s3');

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    connect: {
      server: {
        port: 3000,
        base: '.'
      }
    },
    uglify: {
      app: {
        options: {
          banner: '/*! <%= pkg.name %> v<%= pkg.version %> */'
        },
        files: {
          'dist/babbage.ui.min.js': ['dist/babbage.ui.js']
        }
      },
      deps: {
        options: {},
        files: {
          'dist/deps.js': [
            'bower_components/d3/d3.js',
            'bower_components/d3-plugins/sankey/sankey.js',
            'bower_components/c3js-chart/c3.js',
            'bower_components/angular/angular.js',
            'bower_components/angular-route/angular-route.js',
            'bower_components/angular-bootstrap/ui-bootstrap.min.js',
            'bower_components/angular-bootstrap/ui-bootstrap-tpls.min.js',
            'bower_components/angular-ui-select/dist/select.min.js',
            'bower_components/angular-filter/dist/angular-filter.js'
          ]
        }
      }
    },
    concat: {
      options: {
        banner: 'var ngBabbageGlobals = ngBabbageGlobals || {}; ngBabbageGlobals.embedSite = "http://<%= pkg.deployBucket %>/<%= pkg.deployBase %>/<%= pkg.version %>";',
        stripBanners: true,
        separator: ';'
      },
      dist: {
        src: [ 'dist/templates.js', 'src/app.js', 'src/**/*.js'],
        dest: 'dist/<%= pkg.name %>.js'
      },
    },
    html2js: {
      dist: {
        options: {
          base: '.',
          module: 'ngBabbage.templates',
          rename: function(name) {
            return name.replace('templates', 'babbage-templates');
          },
          htmlmin: {
            collapseWhitespace: true,
            removeComments: true
          }
        },
        src: ['templates/**/*.html'],
        dest: 'dist/templates.js'
      }
    },
    less: {
      app: {
        options: {
          paths: ["less"],
          strictImports: true
        },
        files: {
          "dist/babbage.ui.css": ["less/build.less"]
        }
      },
      embed: {
        options: {
          paths: ["less"],
          strictImports: true
        },
        files: {
          "dist/embed.css": ["less/embed.less"]
        }
      },
      deps: {
        files: {
          "dist/deps.css": ["node_modules/bootstrap/dist/css/bootstrap.css",
                            "bower_components/c3js-chart/c3.css",
                            "bower_components/angular/angular-csp.css",
                            "bower_components/angular-ui-select/dist/select.min.css"]
        }
      }
    },
    aws_s3: {
      assets: {
        options: {
          bucket: '<%= pkg.deployBucket %>',
          region: 'eu-west-1',
          uploadConcurrency: 5
        },
        files: [
          {expand: true, cwd: '.', src: ['dist/**', 'src/**', '*.html'], dest: '/<%= pkg.deployBase %>/<%= pkg.version %>'},
        ]
      }
    },
    watch: {
      templates: {
        files: ['templates/**/*.html'],
        tasks: ['html2js']
      },
      js: {
        files: ['src/**/*.js'],
        tasks: ['concat', 'uglify:app']
      },
      style: {
        files: ['less/**/*.less'],
        tasks: ['less']
      },
    }
  });

  grunt.registerTask('default', ['less', 'html2js', 'concat', 'uglify']);
  grunt.registerTask('deploy', ['aws_s3']);
  grunt.registerTask('server', ['connect', 'watch'])
};
