
// Avoid `console` errors in browsers that lack a console.
(function() {
    var method;
    var noop = function noop() {};
    var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeStamp', 'trace', 'warn'
    ];
    var length = methods.length;
    var console = (window.console = window.console || {});

    while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
    }
}());

$(function (){  //===========================================PLUGINS


	//=======================ENQUIRE.js=====================
	//======================================================


// enquire.js v1.5.4 - Awesome Media Queries in JavaScript
// Copyright (c) 2013 Nick Williams - http://wicky.nillia.ms/enquire.js
// License: MIT (http://www.opensource.org/licenses/mit-license.php)


window.enquire = (function(matchMedia) {

    "use strict";

    /**
     * Helper function for iterating over a collection
     *
     * @param collection
     * @param fn
     */
    function each(collection, fn) {
        var i      = 0,
            length = collection.length,
            cont;

        for(i; i < length; i++) {
            cont = fn(collection[i], i);
            if(cont === false) {
                break; //allow early exit
            }
        }
    }

    /**
     * Helper function for determining whether target object is an array
     *
     * @param target the object under test
     * @return {Boolean} true if array, false otherwise
     */
    function isArray(target) {
        return Object.prototype.toString.apply(target) === "[object Array]";
    }

    /**
     * Helper function for determining whether target object is a function
     *
     * @param target the object under test
     * @return {Boolean} true if function, false otherwise
     */
    function isFunction(target) {
        return typeof target === "function";
    }

    /**
     * Delegate to handle a media query being matched and unmatched.
     *
     * @param {object} options
     * @param {function} options.match callback for when the media query is matched
     * @param {function} [options.unmatch] callback for when the media query is unmatched
     * @param {function} [options.setup] one-time callback triggered the first time a query is matched
     * @param {boolean} [options.deferSetup=false] should the setup callback be run immediately, rather than first time query is matched?
     * @constructor
     */
    function QueryHandler(options) {
        this.initialised = false;
        this.options = options;

        if(!options.deferSetup) {
			this.setup();
		}
    }
    QueryHandler.prototype = {

        /**
         * coordinates setup of the handler
         *
         * @function
         */
        setup : function(e) {
            if(this.options.setup){
                this.options.setup(e);
            }
            this.initialised = true;
        },

        /**
         * coordinates setup and triggering of the handler
         *
         * @function
         * @param [e] the browser event which triggered a match
         */
        on : function(e) {
            if(!this.initialised){
                this.setup(e);
            }
            this.options.match(e);
        },

        /**
         * coordinates the unmatch event for the handler
         *
         * @function
         * @param [e] the browser event which triggered a match
         */
        off : function(e) {
            if(this.options.unmatch){
                this.options.unmatch(e);
            }
        },

        /**
         * called when a handler is to be destroyed.
         * delegates to the destroy or unmatch callbacks, depending on availability.
         *
         * @function
         */
        destroy : function() {
            if(this.options.destroy) {
                this.options.destroy();
            }
            else {
                this.off();
            }
        },

        /**
         * determines equality by reference.
         * if object is supplied compare options, if function, compare match callback
         *
         * @function
         * @param {object || function} [target] the target for comparison
         */
        equals : function(target) {
            return this.options === target || this.options.match === target;
        }

    };
/**
 * Represents a single media query, manages it's state and registered handlers for this query
 *
 * @constructor
 * @param {string} query the media query string
 * @param {boolean} [isUnconditional=false] whether the media query should run regardless of whether the conditions are met. Primarily for helping older browsers deal with mobile-first design
 */
function MediaQuery(query, isUnconditional) {
    this.query = query;
    this.isUnconditional = isUnconditional;
    
    this.handlers = [];
    this.matched = false;
}
MediaQuery.prototype = {

    /**
     * tests whether this media query is currently matching
     *
     * @function
     * @returns {boolean} true if match, false otherwise
     */
    matchMedia : function() {
        return matchMedia(this.query).matches;
    },

    /**
     * add a handler for this query, triggering if already active
     *
     * @function
     * @param {object} handler
     * @param {function} handler.match callback for when query is activated
     * @param {function} [handler.unmatch] callback for when query is deactivated
     * @param {function} [handler.setup] callback for immediate execution when a query handler is registered
     * @param {boolean} [handler.deferSetup=false] should the setup callback be deferred until the first time the handler is matched?
     * @param {boolean} [turnOn=false] should the handler be turned on if the query is matching?
     */
    addHandler : function(handler, turnOn) {
        var qh = new QueryHandler(handler);
        this.handlers.push(qh);

        turnOn && this.matched && qh.on();
    },

    /**
     * removes the given handler from the collection, and calls it's destroy methods
     *
     * @function
     * @param {object || function} handler the handler to remove
     */
    removeHandler : function(handler) {
        var handlers = this.handlers;
        each(handlers, function(h, i) {
            if(h.equals(handler)) {
                h.destroy();
                return !handlers.splice(i,1); //remove from array and exit each early
            }
        });
    },

    /*
     * assesses the query, turning on all handlers if it matches, turning them off if it doesn't match
     *
     * @function
     */
    assess : function(e) {
        if(this.matchMedia() || this.isUnconditional) {
            this.match(e);
        }
        else {
            this.unmatch(e);
        }
    },

    /**
     * activates a query.
     * callbacks are fired only if the query is currently unmatched
     *
     * @function
     * @param {Event} [e] browser event if triggered as the result of a browser event
     */
    match : function(e) {
        if(this.matched) {
			return; //already on
		}

        each(this.handlers, function(handler) {
            handler.on(e);
        });
        this.matched = true;
    },

    /**
     * deactivates a query.
     * callbacks are fired only if the query is currently matched
     *
     * @function
     * @param {Event} [e] browser event if triggered as the result of a browser event
     */
    unmatch : function(e) {
        if(!this.matched) {
			return; //already off
        }

        each(this.handlers, function(handler){
			handler.off(e);
        });
        this.matched = false;
    }
};
    /**
     * Allows for reigstration of query handlers.
     * Manages the  query handler's state and is responsible for wiring up browser events
     *
     * @constructor
     */
    function MediaQueryDispatch () {
        if(!matchMedia) {
            throw new Error('matchMedia is required');
        }

        var capabilityTest = new MediaQuery('only all');
        this.queries = {};
        this.listening = false;
        this.browserIsIncapable = !capabilityTest.matchMedia();
    }

    MediaQueryDispatch.prototype = {

        /**
         * Registers a handler for the given media query
         *
         * @function
         * @param {string} q the media query
         * @param {object || Array || Function} options either a single query handler object, a function, or an array of query handlers
         * @param {function} options.match fired when query matched
         * @param {function} [options.unmatch] fired when a query is no longer matched
         * @param {function} [options.setup] fired when handler first triggered
         * @param {boolean} [options.deferSetup=false] whether setup should be run immediately or deferred until query is first matched
         * @param {boolean} [shouldDegrade=false] whether this particular media query should always run on incapable browsers
         */
        register : function(q, options, shouldDegrade) {
            var queries         = this.queries,
                isUnconditional = shouldDegrade && this.browserIsIncapable,
                listening       = this.listening;

            if(!queries.hasOwnProperty(q)) {
                queries[q] = new MediaQuery(q, isUnconditional);

                this.listening && queries[q].assess();
            }

            //normalise to object
            if(isFunction(options)) {
                options = {
                    match : options
                };
            }
            //normalise to array
            if(!isArray(options)) {
                options = [options];
            }
            each(options, function(handler) {
                queries[q].addHandler(handler, listening);
            });

            return this;
        },

        /**
         * unregisters a query and all it's handlers, or a specific handler for a query
         *
         * @function
         * @param {string} q the media query to target
         * @param {object || function} [handler] specific handler to unregister
         */
        unregister : function(q, handler) {
            var queries = this.queries;

            if(!queries.hasOwnProperty(q)) {
                return this;
            }
            
            if(!handler) {
                each(this.queries[q].handlers, function(handler) {
                    handler.destroy();
                });
                delete queries[q];
            }
            else {
                queries[q].removeHandler(handler);
            }

            return this;
        },

        /**
         * Tests all media queries and calls relevant methods depending whether
         * transitioning from unmatched->matched or matched->unmatched
         *
         * @function
         * @param {Event} [e] if fired as a result of a browser event,
         * an event can be supplied to propagate to the various media query handlers
         */
        fire : function(e) {
            var queries = this.queries,
                mediaQuery;

            for(mediaQuery in queries) {
                if(queries.hasOwnProperty(mediaQuery)) {
                    queries[mediaQuery].assess(e);
				}
            }
            return this;
        },

        /**
         * sets up listeners for resize and orientation events
         *
         * @function
         * @param {int} [timeout=500] the time (in milliseconds) after which the queries should be handled
         */
        listen : function(timeout) {
            var self = this;

            timeout = timeout || 500;

            // any browser that doesn't implement this
            // will not have media query support
            if(!window.addEventListener) {
                return;
            }

            //prevent multiple event handlers
            if(this.listening) {
				return this;
			}

            //creates closure for separate timed events
            function wireFire(event) {
                var timer;

                window.addEventListener(event, function(e) {
                    timer && clearTimeout(timer);

                    timer = setTimeout(function() {
                        self.fire(e);
                    }, timeout);
                });
            }

            //handle initial load then listen
            self.fire();
            wireFire('resize');
            wireFire('orientationChange');

            this.listening = true;
            return this;
        }
    };


    return new MediaQueryDispatch();

}(window.matchMedia));




//================================FOUNDATION REVEAL=========================
//=================================jqeury plugin============================
/*
 * jQuery Reveal Plugin 1.1
 * www.ZURB.com
 * Copyright 2010, ZURB
 * Free to use under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
*/
/*globals jQuery */

(function ($) {
  'use strict';
  //
  // Global variable.
  // Helps us determine if the current modal is being queued for display.
  //
  var modalQueued = false;

  //
  // Bind the live 'click' event to all anchor elemnets with the data-reveal-id attribute.
  //
  $(document).on('click', '[data-reveal-id]', function ( event ) {
    //
    // Prevent default action of the event.
    //
    event.preventDefault();
    //
    // Get the clicked anchor data-reveal-id attribute value.
    //
    var modalLocation = $( this ).attr( 'data-reveal-id' );
    //
    // Find the element with that modalLocation id and call the reveal plugin.
    //
    $( '#' + modalLocation ).reveal( $( this ).data() );

  });

  /**
   * @module reveal
   * @property {Object} [options] Reveal options
   */
  $.fn.reveal = function ( options ) {
      /*
       * Cache the document object.
       */
    var $doc = $( document ),
        /*
         * Default property values.
         */
        defaults = {
          /**
           * Possible options: fade, fadeAndPop, none
           *
           * @property animation
           * @type {String}
           * @default fadeAndPop
           */
          animation: 'fadeAndPop',
          /**
           * Speed at which the reveal should show. How fast animtions are.
           *
           * @property animationSpeed
           * @type {Integer}
           * @default 300
           */
          animationSpeed: 300,
          /**
           * Should the modal close when the background is clicked?
           *
           * @property closeOnBackgroundClick
           * @type {Boolean}
           * @default true
           */
          closeOnBackgroundClick: true,
          /**
           * Specify a class name for the 'close modal' element.
           * This element will close an open modal.
           *
           @example
           <a href='#close' class='close-reveal-modal'>Close Me</a>
           *
           * @property dismissModalClass
           * @type {String}
           * @default close-reveal-modal
           */
          dismissModalClass: 'close-reveal-modal',
          /**
           * Specify a callback function that triggers 'before' the modal opens.
           *
           * @property open
           * @type {Function}
           * @default function(){}
           */
          open: $.noop,
          /**
           * Specify a callback function that triggers 'after' the modal is opened.
           *
           * @property opened
           * @type {Function}
           * @default function(){}
           */
          opened: $.noop,
          /**
           * Specify a callback function that triggers 'before' the modal prepares to close.
           *
           * @property close
           * @type {Function}
           * @default function(){}
           */
          close: $.noop,
          /**
           * Specify a callback function that triggers 'after' the modal is closed.
           *
           * @property closed
           * @type {Function}
           * @default function(){}
           */
          closed: $.noop
        }
    ;
    //
    // Extend the default options.
    // This replaces the passed in option (options) values with default values.
    //
    options = $.extend( {}, defaults, options );

    //
    // Apply the plugin functionality to each element in the jQuery collection.
    //
    return this.not('.reveal-modal.open').each( function () {
        //
        // Cache the modal element
        //
      var modal = $( this ),
        //
        // Get the current css 'top' property value in decimal format.
        //
        topMeasure = parseInt( modal.css( 'top' ), 10 ),
        //
        // Calculate the top offset.
        //
        topOffset = modal.height() + topMeasure,
        //
        // Helps determine if the modal is locked.
        // This way we keep the modal from triggering while it's in the middle of animating.
        //
        locked = false,
        //
        // Get the modal background element.
        //
        modalBg = $( '.reveal-modal-bg' ),
        //
        // Show modal properties
        //
        cssOpts = {
          //
          // Used, when we show the modal.
          //
          open : {
            //
            // Set the 'top' property to the document scroll minus the calculated top offset.
            //
            'top': 0,
            //
            // Opacity gets set to 0.
            //
            'opacity': 0,
            //
            // Show the modal
            //
            'visibility': 'visible',
            //
            // Ensure it's displayed as a block element.
            //
            'display': 'block'
          },
          //
          // Used, when we hide the modal.
          //
          close : {
            //
            // Set the default 'top' property value.
            //
            'top': topMeasure,
            //
            // Has full opacity.
            //
            'opacity': 1,
            //
            // Hide the modal
            //
            'visibility': 'hidden',
            //
            // Ensure the elment is hidden.
            //
            'display': 'none'
          }

        },
        //
        // Initial closeButton variable.
        //
        $closeButton
      ;

      //
      // Do we have a modal background element?
      //
      if ( modalBg.length === 0 ) {
        //
        // No we don't. So, let's create one.
        //
        modalBg = $( '<div />', { 'class' : 'reveal-modal-bg' } )
        //
        // Then insert it after the modal element.
        //
        .insertAfter( modal );
        //
        // Now, fade it out a bit.
        //
        modalBg.fadeTo( 'fast', 0.8 );
      }

      //
      // Helper Methods
      //

      /**
       * Unlock the modal for animation.
       *
       * @method unlockModal
       */
      function unlockModal() {
        locked = false;
      }

      /**
       * Lock the modal to prevent further animation.
       *
       * @method lockModal
       */
      function lockModal() {
        locked = true;
      }

      /**
       * Closes all open modals.
       *
       * @method closeOpenModal
       */
      function closeOpenModals() {
        //
        // Get all reveal-modal elements with the .open class.
        //
        var $openModals = $( ".reveal-modal.open" );
        //
        // Do we have modals to close?
        //
        if ( $openModals.length === 1 ) {
          //
          // Set the modals for animation queuing.
          //
          modalQueued = true;
          //
          // Trigger the modal close event.
          //
          $openModals.trigger( "reveal:close" );
        }

      }
      /**
       * Animates the modal opening.
       * Handles the modal 'open' event.
       *
       * @method openAnimation
       */
      function openAnimation() {
        //
        // First, determine if we're in the middle of animation.
        //
        if ( !locked ) {
          //
          // We're not animating, let's lock the modal for animation.
          //
          lockModal();
          //
          // Close any opened modals.
          //
          closeOpenModals();
          //
          // Now, add the open class to this modal.
          //
          modal.addClass( "open" );

          //
          // Are we executing the 'fadeAndPop' animation?
          //
          if ( options.animation === "fadeAndPop" ) {
            //
            // Yes, we're doing the 'fadeAndPop' animation.
            // Okay, set the modal css properties.
            //
            //
            // Set the 'top' property to the document scroll minus the calculated top offset.
            //
            cssOpts.open.top = $doc.scrollTop() - topOffset;
            //
            // Flip the opacity to 0.
            //
            cssOpts.open.opacity = 0;
            //
            // Set the css options.
            //
            modal.css( cssOpts.open );
            //
            // Fade in the background element, at half the speed of the modal element.
            // So, faster than the modal element.
            //
            modalBg.fadeIn( options.animationSpeed / 2 );

            //
            // Let's delay the next animation queue.
            // We'll wait until the background element is faded in.
            //
            modal.delay( options.animationSpeed / 2 )
            //
            // Animate the following css properties.
            //
            .animate( {
              //
              // Set the 'top' property to the document scroll plus the calculated top measure.
              //
              "top": $doc.scrollTop() + topMeasure + 'px',
              //
              // Set it to full opacity.
              //
              "opacity": 1

            },
            /*
             * Fade speed.
             */
            options.animationSpeed,
            /*
             * End of animation callback.
             */
            function () {
              //
              // Trigger the modal reveal:opened event.
              // This should trigger the functions set in the options.opened property.
              //
              modal.trigger( 'reveal:opened' );

            }); // end of animate.

          } // end if 'fadeAndPop'

          //
          // Are executing the 'fade' animation?
          //
          if ( options.animation === "fade" ) {
            //
            // Yes, were executing 'fade'.
            // Okay, let's set the modal properties.
            //
            cssOpts.open.top = $doc.scrollTop() + topMeasure;
            //
            // Flip the opacity to 0.
            //
            cssOpts.open.opacity = 0;
            //
            // Set the css options.
            //
            modal.css( cssOpts.open );
            //
            // Fade in the modal background at half the speed of the modal.
            // So, faster than modal.
            //
            modalBg.fadeIn( options.animationSpeed / 2 );

            //
            // Delay the modal animation.
            // Wait till the modal background is done animating.
            //
            modal.delay( options.animationSpeed / 2 )
            //
            // Now animate the modal.
            //
            .animate( {
              //
              // Set to full opacity.
              //
              "opacity": 1
            },

            /*
             * Animation speed.
             */
            options.animationSpeed,

            /*
             * End of animation callback.
             */
            function () {
              //
              // Trigger the modal reveal:opened event.
              // This should trigger the functions set in the options.opened property.
              //
              modal.trigger( 'reveal:opened' );

            });

          } // end if 'fade'

          //
          // Are we not animating?
          //
          if ( options.animation === "none" ) {
            //
            // We're not animating.
            // Okay, let's set the modal css properties.
            //
            //
            // Set the top property.
            //
            cssOpts.open.top = $doc.scrollTop() + topMeasure;
            //
            // Set the opacity property to full opacity, since we're not fading (animating).
            //
            cssOpts.open.opacity = 1;
            //
            // Set the css property.
            //
            modal.css( cssOpts.open );
            //
            // Show the modal Background.
            //
            modalBg.css( { "display": "block" } );
            //
            // Trigger the modal opened event.
            //
            modal.trigger( 'reveal:opened' );

          } // end if animating 'none'

        }// end if !locked

      }// end openAnimation


      function openVideos() {
        var video = modal.find('.flex-video'),
            iframe = video.find('iframe');
        if (iframe.length > 0) {
          iframe.attr("src", iframe.data("src"));
          video.fadeIn(100);
        }
      }

      //
      // Bind the reveal 'open' event.
      // When the event is triggered, openAnimation is called
      // along with any function set in the options.open property.
      //
      modal.bind( 'reveal:open.reveal', openAnimation );
      modal.bind( 'reveal:open.reveal', openVideos);

      /**
       * Closes the modal element(s)
       * Handles the modal 'close' event.
       *
       * @method closeAnimation
       */
      function closeAnimation() {
        //
        // First, determine if we're in the middle of animation.
        //
        if ( !locked ) {
          //
          // We're not animating, let's lock the modal for animation.
          //
          lockModal();
          //
          // Clear the modal of the open class.
          //
          modal.removeClass( "open" );

          //
          // Are we using the 'fadeAndPop' animation?
          //
          if ( options.animation === "fadeAndPop" ) {
            //
            // Yes, okay, let's set the animation properties.
            //
            modal.animate( {
              //
              // Set the top property to the document scrollTop minus calculated topOffset.
              //
              "top":  $doc.scrollTop() - topOffset + 'px',
              //
              // Fade the modal out, by using the opacity property.
              //
              "opacity": 0

            },
            /*
             * Fade speed.
             */
            options.animationSpeed / 2,
            /*
             * End of animation callback.
             */
            function () {
              //
              // Set the css hidden options.
              //
              modal.css( cssOpts.close );

            });
            //
            // Is the modal animation queued?
            //
            if ( !modalQueued ) {
              //
              // Oh, the modal(s) are mid animating.
              // Let's delay the animation queue.
              //
              modalBg.delay( options.animationSpeed )
              //
              // Fade out the modal background.
              //
              .fadeOut(
              /*
               * Animation speed.
               */
              options.animationSpeed,
             /*
              * End of animation callback.
              */
              function () {
                //
                // Trigger the modal 'closed' event.
                // This should trigger any method set in the options.closed property.
                //
                modal.trigger( 'reveal:closed' );

              });

            } else {
              //
              // We're not mid queue.
              // Trigger the modal 'closed' event.
              // This should trigger any method set in the options.closed propety.
              //
              modal.trigger( 'reveal:closed' );

            } // end if !modalQueued

          } // end if animation 'fadeAndPop'

          //
          // Are we using the 'fade' animation.
          //
          if ( options.animation === "fade" ) {
            //
            // Yes, we're using the 'fade' animation.
            //
            modal.animate( { "opacity" : 0 },
              /*
               * Animation speed.
               */
              options.animationSpeed,
              /*
               * End of animation callback.
               */
              function () {
              //
              // Set the css close options.
              //
              modal.css( cssOpts.close );

            }); // end animate

            //
            // Are we mid animating the modal(s)?
            //
            if ( !modalQueued ) {
              //
              // Oh, the modal(s) are mid animating.
              // Let's delay the animation queue.
              //
              modalBg.delay( options.animationSpeed )
              //
              // Let's fade out the modal background element.
              //
              .fadeOut(
              /*
               * Animation speed.
               */
              options.animationSpeed,
                /*
                 * End of animation callback.
                 */
                function () {
                  //
                  // Trigger the modal 'closed' event.
                  // This should trigger any method set in the options.closed propety.
                  //
                  modal.trigger( 'reveal:closed' );

              }); // end fadeOut

            } else {
              //
              // We're not mid queue.
              // Trigger the modal 'closed' event.
              // This should trigger any method set in the options.closed propety.
              //
              modal.trigger( 'reveal:closed' );

            } // end if !modalQueued

          } // end if animation 'fade'

          //
          // Are we not animating?
          //
          if ( options.animation === "none" ) {
            //
            // We're not animating.
            // Set the modal close css options.
            //
            modal.css( cssOpts.close );
            //
            // Is the modal in the middle of an animation queue?
            //
            if ( !modalQueued ) {
              //
              // It's not mid queueu. Just hide it.
              //
              modalBg.css( { 'display': 'none' } );
            }
            //
            // Trigger the modal 'closed' event.
            // This should trigger any method set in the options.closed propety.
            //
            modal.trigger( 'reveal:closed' );

          } // end if not animating
          //
          // Reset the modalQueued variable.
          //
          modalQueued = false;
        } // end if !locked

      } // end closeAnimation

      /**
       * Destroys the modal and it's events.
       *
       * @method destroy
       */
      function destroy() {
        //
        // Unbind all .reveal events from the modal.
        //
        modal.unbind( '.reveal' );
        //
        // Unbind all .reveal events from the modal background.
        //
        modalBg.unbind( '.reveal' );
        //
        // Unbind all .reveal events from the modal 'close' button.
        //
        $closeButton.unbind( '.reveal' );
        //
        // Unbind all .reveal events from the body.
        //
        $( 'body' ).unbind( '.reveal' );

      }

      function closeVideos() {
        var video = modal.find('.flex-video'),
            iframe = video.find('iframe');
        if (iframe.length > 0) {
          iframe.data("src", iframe.attr("src"));
          iframe.attr("src", "");
          video.fadeOut(100);  
        }
      }

      //
      // Bind the modal 'close' event
      //
      modal.bind( 'reveal:close.reveal', closeAnimation );
      modal.bind( 'reveal:closed.reveal', closeVideos );
      //
      // Bind the modal 'opened' + 'closed' event
      // Calls the unlockModal method.
      //
      modal.bind( 'reveal:opened.reveal reveal:closed.reveal', unlockModal );
      //
      // Bind the modal 'closed' event.
      // Calls the destroy method.
      //
      modal.bind( 'reveal:closed.reveal', destroy );
      //
      // Bind the modal 'open' event
      // Handled by the options.open property function.
      //
      modal.bind( 'reveal:open.reveal', options.open );
      //
      // Bind the modal 'opened' event.
      // Handled by the options.opened property function.
      //
      modal.bind( 'reveal:opened.reveal', options.opened );
      //
      // Bind the modal 'close' event.
      // Handled by the options.close property function.
      //
      modal.bind( 'reveal:close.reveal', options.close );
      //
      // Bind the modal 'closed' event.
      // Handled by the options.closed property function.
      //
      modal.bind( 'reveal:closed.reveal', options.closed );

      //
      // We're running this for the first time.
      // Trigger the modal 'open' event.
      //
      modal.trigger( 'reveal:open' );

      //
      // Get the closeButton variable element(s).
      //
     $closeButton = $( '.' + options.dismissModalClass )
     //
     // Bind the element 'click' event and handler.
     //
     .bind( 'click.reveal', function () {
        //
        // Trigger the modal 'close' event.
        //
        modal.trigger( 'reveal:close' );

      });

     //
     // Should we close the modal background on click?
     //
     if ( options.closeOnBackgroundClick ) {
      //
      // Yes, close the modal background on 'click'
      // Set the modal background css 'cursor' propety to pointer.
      // Adds a pointer symbol when you mouse over the modal background.
      //
      modalBg.css( { "cursor": "pointer" } );
      //
      // Bind a 'click' event handler to the modal background.
      //
      modalBg.bind( 'click.reveal', function () {
        //
        // Trigger the modal 'close' event.
        //
        modal.trigger( 'reveal:close' );

      });

     }

     //
     // Bind keyup functions on the body element.
     // We'll want to close the modal when the 'escape' key is hit.
     //
     $( 'body' ).bind( 'keyup.reveal', function ( event ) {
      //
      // Did the escape key get triggered?
      //
       if ( event.which === 27 ) { // 27 is the keycode for the Escape key
         //
         // Escape key was triggered.
         // Trigger the modal 'close' event.
         //
         modal.trigger( 'reveal:close' );
       }

      }); // end $(body)

    }); // end this.each

  }; // end $.fn

} ( jQuery ) );



//==================================RIOTRY LEARY============================
//=================================jqeury plugin============================

// jQuery.leary.js v1 - Simple dropdown methods in jQuery
// Copyright (c) 2013 Paul Rivera - riotry.com
//=================================================================================

 (function($) {

   'use strict';   //   ;_;  
   
    //==================================================
   // @PARENT CONSTRUCTOR
  //====================================================
    var Timothy = function($element,$triggerEl,togSpeed) {

      if (! $triggerEl) this.$trigger = null;
      else this.$trigger = $triggerEl; 
        this.$dropEl = $element; 
          this.speed = togSpeed;
      this.$checkElement = [this.$dropEl,this.$trigger];
    };

          //@TOGGLEIN
          //==========================================
          //rfouneturns a simple toggle function 
          //for the dropdown element
            Timothy.prototype.toggleIn = function() {
                var that = this;
                        return that.$dropEl.toggle(that.speed);
            };


          //@CLOSE IF OUTSIDE
          //==========================================
          //binds a hover event to the both the trigger and drop elements
          //to check if a click event happends on them 
          //if it happens outside of them it triggers hide().

          Timothy.prototype.closeIfOutside = function() {
            var that = this;
            var mouseIsInside = false;
            var mouseInTrigger = false;
            
                $(that.$dropEl).hover(function(){ 
                                        //The mousup seems to happen firs tthen the toggle jumps in and changes it back.
                    mouseIsInside=true; //it seems like the click is happening second 
                }, function(){ 
                    mouseIsInside=false; 
                });

            /*
                $(that.$trigger).hover(function(){ 
                    mouseInTrigger=true; 
                }, function(){ 
                     mouseInTrigger=false; 
                });
            */
                $('body').bind('mouseup',function(){ 
                  //if(mouseInTrigger) { mouseIsInside = true; console.log(that.$trigger);}//why? WHY!? WHY!!
                  if(! mouseIsInside) {that.$dropEl.hide(that.speed);}
                });
          } 


          //@ACTIVATE ICON
          //==========================================
          //Binds a click element to the Trigger element
          //Cheks the dropdowns css display
          //if its in displaying (block elment) 
          //add activate class to icon:beofore(in scss)
          //else Remove that class

          Timothy.prototype.activateIc = function(activeClass){
            var that = this;
            
            $('body').bind('click', function (){
              that.$dropEl.css('display') === 'block'?
                    that.$trigger.addClass(activeClass): 
                    that.$trigger.removeClass(activeClass);
            }); 
          }


   // SETTINGS
  //=================================================================================

  var methods = {

    init: function(options) {
      // Repeat over each element in selector
      return this.each(function() {
        var $this = $(this); 
        var settings = $this.data('leary');

        if(typeof(settings) === 'undefined') {
          //========================================@SETTINGS
          var defaults = {
            target : $this,
            trigger : null,
            activeClass : null,
            speed : null ,
            kill : false ,
            checkOutside :false
          };

          settings = $.extend(defaults, options);
          // Save our newly created settings
          $this.data('leary', settings);
        } else {
          settings = $.extend(settings, options);
          $this.data('leary', settings);
        }

        //RUNNING CODE ============================@INIT METHOD
        if (settings.kill === false) {

            var dropdown = new Timothy(settings.target,settings.trigger,settings.speed);
            dropdown.toggleIn();

            if(settings.checkOutside && settings.trigger) {
              dropdown.closeIfOutside();
            }

            
            if (settings.trigger && settings.activeClass) { 
              dropdown.activateIc(settings.activeClass);
            }
            

        } else { return false };

      });
    },

    revive : function (options) { 
      return $(this).each(function() {
            var $this = $(this);
            var savedSettings = $this.data('leary');
            var newSettings = $.extend({}, savedSettings, options);
            var data = $this.data('leary', newSettings);

        //RUNNING CODE ============================@REVIVE METHOD
            newSettings.kill = false;
      });
    },

    kill : function(options) {
      return $(this).each(function() {
            var $this = $(this);
            var savedSettings = $this.data('leary');
            var newSettings = $.extend({}, savedSettings, options);
            var data = $this.data('leary', newSettings);

        //RUNNING CODE ============================@KILL METHOD
            newSettings.kill = true;
            $this.hide(newSettings.speed);
      });
    }
  };//End Methods object


    $.fn.leary = function(method) { 
      
        if ( methods[method] ) {  //if methods
            return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.leary' );
        }
      
    };
})(jQuery);


});//================================PLUGINS CLOSE=============================




