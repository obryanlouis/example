

$(function ($) {

'use strict';   //   ;_; 

//Django Security ===================================================

$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


//===============================GLOBAL CLASSES====================================
//=================================================================================



	  //==============================================================
	 // @SPIDEY CONSTRUCTOR CLASS
	//==============================================================
	 var Spidey = function (dataEl) {
	 	//Grabs data name passed and archives it 
	 	
	    var dataTag  = dataEl;
	    var $dataTag = $('['+ dataEl +']');

	    //Cache document
		this.$doc = $(document);

		//into an object  (so the class can be $.extend(ed) later if needed)
	    this.elData = {
	    	dataTag : dataTag,
	    	$dataTag : $dataTag,
	    }
	 }
	 			 //===============
			    // HELPER METHOD
			   //============================================================
			  // spidey @CALLER METHOD
			 //==============================================================
			 Spidey.prototype.caller = function (methodCalled){
			 	//Chooses a method to call depending on its parameter.
			 	//needs to be updated whenever new functions are called.


			 	switch(methodCalled){

			 		case 'formJack':
						this.formJack();
			 		break;

			 		case 'toggleIdEl':
			 			this.toggleIdEl();
			 		break;

			 		case 'learyNoti':
			 			this.learyNoti();
			 			console.log( "this.learyNoti();")
			 		break;

			 		case 'learyList':
			 			this.learyList();
			 			console.log( "this.learyList();")
			 		break;

			 		case 'learyBasic':
			 			this.learyBasic();
			 			console.log( "this.learyBasic();")
			 		break;

			 		default: 
			 			return false;
			 	}

			 }

			 	//===============
			   // ACTION METHODS
			  //============================================================
			 // spidey action @CLICKSPIDER METHOD
			//==============================================================
			 Spidey.prototype.clickSpider = function(methodCall){
			 //checks for the id of the clicked elment and then trigers a function with that id
			 	var that = this;

			 	this.$doc.on('click','['+ that.elData.dataTag +']', function() {
			 		
			 		//Get the atribute name of the data Tag
			 		that.idName = $( this ).attr( that.elData.dataTag );

			 		//we need this action to call the method in the param
			 		return that.caller(methodCall);

			 	});
			 }

			  //============================================================
			 // spidey action @HOVERSPIDER METHOD
			//==============================================================
			 Spidey.prototype.hoverSpider = function(methodCall){
			 //checks for the id of the clicked elment and then trigers a function with that id
			 	var that = this;

			 	this.$doc.on('hover','['+ that.elData.dataTag +']', function(event) {
			 		
			 		//Get the atribute name of the data Tag
			 		that.idName = $( this ).attr( that.elData.dataTag );
		
			 			return that.caller(methodCall);
			 	
			 	});
			 }


			  //============================================================
			 // spidey @FORMJACK METHOD
			//==============================================================
		 	Spidey.prototype.formJack = function() {
		 	// Hijacks corresponding forms to work while being invisible 
			// in the invible_forms_global || feature block)
		 	//This function is already being triggered by an Action method

			 	var $trigger = this.elData.$dataTag,
			 		$input 	 = $('#'+this.idName),
			 		$submit	 = $('[name='+this.idName+']');

			 	 // Will be called depending on the action method that calls it
			 	// triggering a click on the input form corresponding to the id
			 	$input.trigger('click');

			 	 // Submit as soon as user clicks open on browse window 
			 	// by Detecting changes in the form element
			 	$input.change(function(){	
			 		$submit.trigger('click');
			 	});
		 	};

		 	  //============================================================
			 // spidey @TOGGLEIDEL METHOD
			//==============================================================
		 	Spidey.prototype.toggleIdEl = function() {
		 	// Grabs the id element (found in the value of the data="" attribute)
		 	// And triggers jqeury toggle on it

			 	var $trigger    = this.elData.$dataTag,
			 		$idElement  = $('#'+this.idName);
			 
			 	 // Will be called depending on the action method that calls it
			 	// triggering a click on the input form corresponding to the id
			 	$idElement.toggle();
		 	};

		 	  //============================================================
			 // spidey @LEARY CALLS
			//==============================================================

		 		Spidey.prototype.learyNoti = function(){
					var $drop = $('#'+this.idName);
				 	$drop.leary({
            			trigger : this.elData.$daTag,
            			activeClass : 'active_dropdown',
            			speed : null,
            			checkOutside :true
				 	});
				}

				Spidey.prototype.learyList = function(){
					var $drop = $('#'+this.idName);
					$drop.leary({
						trigger : this.elData.$dataTag,
						speed : 'fast'
					});
				}

				Spidey.prototype.learyBasic = function(){
					var $drop = $('#'+this.idName);
					$drop.leary({
						trigger : this.elData.$dataTag,
						checkOutside : true
					});
				}



//===============================FUNCTIONS=========================================
//=================================================================================

	var submitCloseModal = function($modal,$button){
		$button.click(function(){
			$modal.trigger('reveal:close');	
		});
	}
	

	/////////////////////////////ROUGH AJAX FUNCTION////////////////////////////////
	//==============================================================================
	
	//inptus used can be an array or an object that stores what the inputs in that 
	//form are.

  	var ajaxTesxtPost = function(urlUsed, $formUsed) {

		// VARIABLE TO HOLD REQUEST
		var request, 
			url = urlUsed,
			$form = $formUsed;
		
		// BIND TO THE SUBMIT EVENT OF A FORM
		$form.submit(function(event){

		    // ABORT ANY PENDING REQUEST
		    if (request) {
		        request.abort();
		    }
			var $form = $(this);
			/*
	  		var $inputsUsed = new Array();

	  		for(var i in inputsUsed) {
	  			$inputsUsed = $form.find(inputsUsed[i])
	  			// let's disable the inputs for the duration of the ajax request
		        $inputsUsed[i].prop("disabled", true);
	  		}
			*/
			var serializedData = $form.serialize();
			
		    // fire off the request to /ajax_test/
		    var request = $.ajax({
		        url: urlUsed,
		        type: "POST",
		        data: serializedData,
		        //dataType: "json",
		        success : function(){
		        console.log(serializedData);
		        }
		    });

		    // callback handler that will be called on success
		    request.done(function (response, textStatus, jqXHR){
		        // log a message to the console
		        console.log("Hooray, it worked!");
		    });

		    // callback handler that will be called on failure
		    request.fail(function (jqXHR, textStatus, errorThrown){
		        // log the error to the console
		        console.error(
		            "The following error occured: "+
		            textStatus, errorThrown
		        );
		    });

			/*
		    // callback handler that will be called regardless
		    // if the request failed or succeeded
		    request.always(function () {
		        // reenable the inputs
		        for(var i in inputsUsed){
		           $inputsUsed[i].prop("disabled", false);
				   console.log('inputs enabled');
	  			}
		    });
			*/
		    // prevent default posting of form
		    event.preventDefault();
		});
 	}







//===============================BASE APP JS=======================================
//=================================================================================


	//@VARIABLES
	//=======================================================
	//-------------------------------------DROPDOWN VARIABLES

	var $notiTriggerElement 	= [$('#inboxDropdownTrigger'),
								   $('#notesDropdownTrigger'),
								   $('#connectionDropdownTrigger')];

	var $notiDropdownElement	= [$('#inboxDropdown'),
								   $('#notesDropdown'),
								   $('#connectDropdown')];

	var $listTriggerElement = [$('#brandsListTrigger'), 
							   $('#doingsListTrigger')];
	
	var $listDropdownElement 	= [$('#brandsList'),
							  		 $('#doingsList')];

	var $accountTriggerElement   =  $('#userDropdownTrigger');
	var $accountDropdownElement  =  $('#userDropdown');


	var $uploadTriggerElement = $('[data-type="uploadDropdownTrigger"]');
	var $uploadDropdownElement = $('[data-type="uploadButtonDropdown"]');


	//----------------------------------------MODAL VARIABLES
	//	WHEN ON MOBILE MODE TEST
	//	CHECK FOR BROWSER SIZE 

	var desktopSizeMin		= 850;
	var tabletSizeMax 		= desktopSizeMin;
	var mobileSizeMax 		= 480;


	//=======================================================
	//================= LOCAL FUNCTIONS  ====================
	//=======================================================

	var learyCall = function($trigger,$drop,speed,aClass,checkOut) {
		$trigger.click(function(){
			$drop.leary({
				trigger: $trigger,
				activeClass : aClass,
				checkOutside : checkOut,
				speed : speed
			});
		});
	}






	//=======================================================
	//================= CALL DROPDOWNS ======================
	//=======================================================

	/*
	//HEADER DROPDOWNS
	for(var i in $notiTriggerElement) {
		learyCall($notiTriggerElement[i],$notiDropdownElement[i],null,'active_dropdown',true);
	}
	learyCall($accountTriggerElement,$accountDropdownElement,null, null,true);
	
	//BODY DROPDOWNS
	for(var i in $listTriggerElement) {
		learyCall($listTriggerElement[i],$listDropdownElement[i],'slow',null, false);
	}
	learyCall($uploadTriggerElement,$uploadDropdownElement,'fast',null,false);
	*/

	//=======================================================
	//================= CALL SPIDERS ========================
	//=======================================================

	//Attatch functions an run them (when assigned in their methods)
	//to all the elements with the proper data- attributes

	//HIJACK ALL INPUT=FILE forms to be triggered by assinged buttons
	var FormHijacks = new Spidey('data-trigger-browse-id');
	FormHijacks.clickSpider('formJack');

	//show
	var showOnhover = new Spidey('data-trigger-hover-toggle');
	showOnhover.hoverSpider('toggleIdEl');
   
   	//LEARY DROPDOWN FOR NOTIFICATIONS
   	var learyNoti = new Spidey('data-leary-noti');
   	learyNoti.clickSpider('learyNoti');

   	//LEARY DROPDOWN FOR LIST 
   	var learyList = new Spidey('data-leary-list');
   	learyList.clickSpider('learyList');

   	//LEARY DROPDOWN FOR BASIC DROPDOWN
   	var learyBasic = new Spidey('data-leary-basic');
   	learyBasic.clickSpider('learyBasic');

	//=======================================================
	//==============  CALLs MODAL RElATED ===================
	//=======================================================

	var $allModals =  [$('#videoUploadModal'),
						$('#imagesUploadModal'),
						$('#audioUploadModal'),
						$('#textUploadModal')],
		$submitButtons = $('input[name*="submit"]');

	for (var i=0; i<$allModals.length-1; i++){
		submitCloseModal($allModals[i],$submitButtons);
	};

	//=======================================================
	//==================== CALL AJAX ========================
	//=======================================================


	var ajaxURL = ['/backboard/'],
		$form 	 = [$('form#text_upload'),
					$('form#image_info_formset'),
					$('form#video_info_form'),
					$('form#audio_info_form')];
		
	for (var i in $form){
		ajaxTesxtPost(ajaxURL[0], $form[i]);
	}



	//@TOGGLE NAV BUTTON
	//=======================================================
	$('[data-type="navCallButton"]').bind('click', function(){
		$('[data-type="navCollapseControl"]').toggle('fast');
		$('[data-type="search_home_band"]').toggle('100');
		$('[data-type="upload_plus_icon2"]').toggle();
	});


    //====================@MEDIA CALLS======================
	//==============Using enquire plugin to=================
	//==============trigger on browser change===============
	//==================for backb_global====================


	enquire.register("screen and (max-width:"+mobileSizeMax+"px)", { 

	//=======================================================
	//=================MOBILE STATE CHANGE===================
	//=======================================================
	

	    match : function() {

			$('body').removeClass('tabletOn');
			$('body').addClass('mobileOn');
			$('[data-type="restOfHeader"]').hide();
			$('[data-type="navCollapseControl"]').hide();
			$('[data-type="navCallButton"]').show();
			$('header.band').css({ 'min-width': '200px' });
			$('[data-type="search_home_band"]').hide();		//hide search band

			//kill header drops
			for(var i in $notiDropdownElement) {$notiDropdownElement[i].leary('kill');}
			$accountDropdownElement.leary('kill');


	    },      

	    unmatch : function() {
	    	$('body').removeClass('mobileOn');			//Take off mobilOn class
	    	
	    	//Revive header drops
			for(var i in $notiDropdownElement) {$notiDropdownElement[i].leary('revive');}
			$accountDropdownElement.leary('revive');
	    }

	}).register("screen and (min-width:"+mobileSizeMax+"px) and (max-width:"+tabletSizeMax+"px)", {
		

	//=======================================================
	//=================TABLET STATE CHANGE===================
	//=======================================================


	    match : function() {

	    	$('body').addClass('tabletOn'); 				//add tablet class to body
	    	$('body').removeClass('mobileOn');				//Take off mobilOn class
	    	$('[data-type="navCallButton"]').show();		//show the Nav Toggle button
	    	$('[data-type="restOfHeader"]').hide(); 		//collapse big screen
	    	$('[data-type="navCollapseControl"]').hide();	//hide navbar
	    	$('[data-type="navCallButton"]').show();		//show Mobile items
	    	$('header.band').css({ 'min-width': tabletSizeMax+'px' })	////Change min-width of containers //consider using arrray
	    	$('[data-type="search_home_band"]').hide();		//hide search band

	    	
	    },      
	    unmatch : function() {
	    	$('body').removeClass('tabletOn');				//remove tablet class from body
	    }

	}).register("screen and (min-width:"+desktopSizeMin+"px)", {

	//=======================================================
	//=================DESKTOP STATE CHANGE==================
	//=======================================================

	    match : function() {

	    	$('body').removeClass('mobileOn tabletOn');
	    	$('[data-type="navCallButton"]').hide();			//hide nav toggle button
	    	$('[data-type="restOfHeader"]').show();				//show right side of header
	    	$('[data-type="navCollapseControl"]').show();		//show col
	    	$('[data-type="search_home_band"]').hide();      	//hide search band

	    },      
	    unmatch : function() {
	    	$('[data-type="navCollapseControl"]').hide();

	    }
	}).listen(1); //END ENQUIERE CHECK


});





