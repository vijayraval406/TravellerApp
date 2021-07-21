$(function () {
	var DATE_FORMAT = 'm/d/yy';
  var $datepicker = $('.js-datepicker-inline');
  
	$datepicker.datepicker({
    format: DATE_FORMAT,
    /* startDate: new Date(),
    templates: {
        leftArrow: '<i class="fa fa-chevron-left"></i>',
        rightArrow: '<i class="fa fa-chevron-right"></i>'
    } */
  });
});