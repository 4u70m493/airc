$(document).ready(function(){
    var countries=[];

    function loadCountries(){
        $.getJSON('/countries', function(data, status, xhr){
            for (var i = 0; i < data.length; i++ ) {
                countries.push(data[i].name);
            }
        });
    };

    loadCountries();
    $( "#country_ac" ).autocomplete({
        source: countries
    });
});