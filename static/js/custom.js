// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();


$('.custom_slick_slider').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    dots: true,
    fade: true,
    adaptiveHeight: true,
    asNavFor: '.slick_slider_nav',
    responsive: [{
        breakpoint: 768,
        settings: {
            dots: false
        }
    }]
})

$('.slick_slider_nav').slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    asNavFor: '.custom_slick_slider',
    centerMode: false,
    focusOnSelect: true,
    variableWidth: true
});

function semester_routing() {
    var semester = document.getElementById('semester-select').value;
    var loc = 'http://127.0.0.1:5000/Courses/' + semester;
    location.assign(loc);
}

function course_code_routing() {
    var course_code = document.getElementById('course-code').value;
    var loc = 'http://127.0.0.1:5000/Courses/' + course_code;
    location.assign(loc);
}

function calendar_routing() {
    var semester = document.getElementById('semester-select2').value;
    var loc = 'http://127.0.0.1:5000/Schedule/' + semester;
    location.assign(loc);
    alert("DO NOT REFRESH THE PAGE!\nPlease wait while the schedule is being generated.\nIt may take a few minutes.");
}