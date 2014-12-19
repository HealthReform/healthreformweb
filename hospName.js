var casper = require('casper').create();
var links = [];
var hospitalName = ''

function getLinks() {
    var links = document.querySelectorAll('h3.r a');
    return Array.prototype.map.call(links, function(e) {
        return e.getAttribute('href');
    });
}


casper.start('http://www.healthcarereportcard.illinois.gov', function() {

});


casper.then(function() {
    var hospitalName = casper.cli.get(0);
    //this.echo(this.getCurrentUrl());
    this.fillSelectors('form#SearchFacilityNameForm', {
         'input[id = "SearchFacilityName"] ' : hospitalName
    }, true);
    

    //this.click('.float-left ui-icon ui-icon-search');
    
});
casper.then(function(){
    //this.echo(this.getCurrentUrl());
    this.click(" a[href*='/hospitals/'] ");

});
casper.run(function() {
    //this.echo(this.getCurrentUrl());
    
    this.echo(this.fetchText('h1.entity-name'));
    this.exit();
});