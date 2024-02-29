(function ($) {
 "use strict";
 
 //defaults
   $.fn.editable.defaults.url = '/post'; 
	
    //enable / disable
   $('#enable').click(function() {
       $('#user .editable').editable('toggleDisabled');
   });    
   
   $('#meeting_start').editable({
        format: 'yyyy-mm-dd hh:ii',    
        viewformat: 'dd/mm/yyyy hh:ii',
        validate: function(v) {
           if(v && v.getDate() == 10) return 'Day cant be 10!';
        },
        datetimepicker: {
           todayBtn: 'linked',
           weekStart: 1
        }        
    });            
    
	 
    
    //editables 
    $('#username').editable({
           url: '/post',
           type: 'text',
           pk: 1,
           name: 'username',
           title: 'Enter username'
    });
    
    $('#firstname').editable({
        validate: function(value) {
           if($.trim(value) == '') return 'This field is required';
        }
    });
    
    $('#sex').editable({
        prepend: "not selected",
        source: [
            {value: 1, text: 'Male'},
            {value: 2, text: 'Female'}
        ],
        display: function(value, sourceData) {
             var colors = {"": "gray", 1: "green", 2: "blue"},
                 elem = $.grep(sourceData, function(o){return o.value == value;});
                 
             if(elem.length) {    
                 $(this).text(elem[0].text).css("color", colors[value]); 
             } else {
                 $(this).empty(); 
             }
        }   
    });    
    
    $('#status').editable();   
    
    $('#group').editable({
       showbuttons: true 
    });    
    
    $('#group1').editable({
       showbuttons: false 
    });   
    $('#group2').editable({
       showbuttons: false 
    });   
    $('#group3').editable({
       showbuttons: false 
    });   
    $('#group4').editable({
       showbuttons: false 
    });   
    $('#group5').editable({
       showbuttons: false 
    });   
	
    $('#vacation').editable({
        datepicker: {
            todayBtn: 'linked'
        } 
    });  
        
     $('#dob').editable();  
    $('#event').editable({
        placement: 'right',
        combodate: {
            firstItem: 'name'
        }
    });    
    
    
    $('#comments').editable({
        showbuttons: 'bottom'
    }); 
    
    $('#note').editable(); 
    $('#pencil').on('click', function(e) {
        e.stopPropagation();
        e.preventDefault();
        $('#note').editable('toggle');
   });   
   
   
   
   $('#fruits').editable({
       pk: 1,
       limit: 3,
       source: [
        {value: 1, text: 'banana'},
        {value: 2, text: 'peach'},
        {value: 3, text: 'apple'},
        {value: 4, text: 'watermelon'},
        {value: 5, text: 'orange'}
       ]
    }); 
      
    $('#tags').editable({
        inputclass: 'input-large',
        select2: {
            tags: ['html', 'javascript', 'css', 'ajax'],
            tokenSeparators: [",", " "]
        }
    });   

    var countries = [];
    $.each({"BD": "Bangladesh", "BE": "Belgium", "BF": "Burkina Faso", 
    "BG": "Bulgaria", "BA": "Bosnia and Herzegovina", "BB": "Barbados",
     "WF": "Wallis and Futuna", "BL": "Saint Bartelemey", "BM": "Bermuda",
      "BN": "Brunei Darussalam", "BO": "Bolivia", "BH": "Bahrain", "BI": "Burundi", 
      "BJ": "Benin", "BT": "Bhutan", "JM": "Jamaica", "BV": "Bouvet Island", "BW": 
      "Botswana", "WS": "Samoa", "BR": "Brazil", "BS": "Bahamas", "JE": "Jersey" }, function(k, v) {
        countries.push({id: k, text: v});
    }); 
    $('#country').editable({
        source: countries,
        select2: {
            width: 200,
            placeholder: 'Select country',
            allowClear: true
        } 
    });      

 
   
   
})(jQuery); 