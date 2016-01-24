var gulp = require('gulp');
var $ = require('gulp-load-plugins')();
var browserSync = require('browser-sync');

var autoprefixerOptions = {
    browsers: ['last 2 versions', '> 5%']
};

gulp.task('browser-sync', ['sass'], function() {
    var files = [
        'static/js/*.js',
        'static/css/*.css',
        'templates/*.html',
        'index.html'
    ];

    browserSync.init(files, {
        server: {baseDir: "./"}
    });
});

gulp.task('3rd-css', function() {
    return gulp.src('static/3rd-css/*.css')
        .pipe($.concatCss("3rd-css-all.css"))
        .pipe(gulp.dest('static/css/'))
        .pipe(browserSync.stream());
});

gulp.task('sass', function() {
  return gulp.src('static/scss/*.scss')
        .pipe($.sass().on('error', $.sass.logError))
        .pipe($.autoprefixer(autoprefixerOptions))
        .pipe(gulp.dest('static/css/'))
        .pipe(browserSync.stream());
});

gulp.task('default', ['sass', '3rd-css', 'browser-sync'], function() {
    gulp.watch("static/3rd-css/*.css", ['3rd-css']);
    gulp.watch("static/scss/*.scss", ['sass']);
});

gulp.task('build', ['sass', '3rd-css']);
