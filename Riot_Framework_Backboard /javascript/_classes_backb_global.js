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
			    // final comand in class
			   //============================================================
			  // spidey @CALLER METHOD
			 //==============================================================
			 Spidey.prototype.caller = function (methodCalled){
			 	//Chooses a method to call depending on its parameter.

			 	//make into switch as it grows 
			 	if(methodCalled === 'formJack'){
			 		this.formJack();
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
			 		
			 		that.idName = $( this ).attr( that.elData.dataTag );

			 		//we need this action to call the method in the param
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