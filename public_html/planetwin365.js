var page = require('webpage').create();
var args = require('system').args;
var fs = require('fs');
var address = args[1];
var outfile = args[2];
var user_agent = args[3];
page.settings.userAgent = user_agent;
page.open(address, function(){
	fs.write(outfile, page.content, 'w');
	phantom.exit();
});
