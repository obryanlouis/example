
/* -------------------@SECTION TOGGLE----------------------------*/
$(function () {

	//TOGGLES LOGIN ON
		$('#tog1').addClass("highlightTog");
	$('#tog1').click(function() {
		$(this).addClass("highlightTog");
		$('#tog2').removeClass("highlightTog");
		$('.loginSecTog').show('fast');
		$('#registerSec').hide('600');
	});
	//TOGGLES @REGISTER ON
		$('#tog2').click(function() {
		$(this).addClass("highlightTog");
		$('#tog1').removeClass("highlightTog");
		$('.loginSecTog').hide('600');
		$('#registerSec').show('fast');
	});
	//Activates CHOSEN Plugin
		$('.chzn-slct-gender').chosen({disable_search:true});
		$('.chzn-slct-month').chosen({disable_search:true});
		$('.chzn-slct-day').chosen({disable_search:true});
		$('.chzn-slct-year').chosen({disable_search:true});
		$('.chzn-slct-country').chosen({disable_search:true});
/*-------------------@FORM DESCRIPTIONS POP UPS ----------------------------*/
    //Activate the @LOCATION description
	$('input#id_city, input#id_state, div#cntry').click().focusin(function(){
		$('.descLocation').slideDown('200');
	});
	//Activate the @DATE OF BIRTH description
	$('div#date').click().focusin(function(){
		$('.descDOB').slideDown('200');
		$('a#whyLink').slideDown('200');
	});
	//HIDE the LOCATION description
	$('input#id_first_name,input#id_middle_name, input#id_last_name,div#gend,div#date').click(function(){
		$('.descLocation:visible').slideUp();
		});
	//HIDE the LOCATION description
	$('input#id_first_name,input#id_middle_name, input#id_last_name,div#gend,div#cntry,input#id_city, input#id_state').click(function(){
		$('.descDOB:visible').slideUp();
		$('a#whyLink:visible').slideUp();
		});
/*-----------------@PLACEHOLDER for password reset -----------------------*/
	$('#id_email').click(function(){
		$('span#plcehld').hide();
	});
});


















