/**
 * Copyright (c)2005-2009 Matt Kruse (javascripttoolbox.com)
 * 
 * Dual licensed under the MIT and GPL licenses. 
 * This basically means you can use this code however you want for
 * free, but don't claim to have written it yourself!
 * Donations always accepted: http://www.JavascriptToolbox.com/donate/
 * 
 * Please do not link to the .js files on javascripttoolbox.com from
 * your site. Copy the files locally to your server instead.
 * 
 */
// Constructor
function CheckBoxGroup() {
	this.controlBox=null;
	this.controlBoxChecked=null;
	this.maxAllowed=null;
	this.maxAllowedMessage=null;
	this.masterBehavior="all";
	this.formRef=null;
	this.checkboxWildcardNames=new Array();
	this.checkboxNames=new Array();
	this.totalBoxes=0;
	this.totalSelected=0;
	// Public methods
	this.setControlBox=CBG_setControlBox;
	this.setMaxAllowed=CBG_setMaxAllowed;
	this.setMasterBehavior=CBG_setMasterBehavior;	// all, some
	this.addToGroup=CBG_addToGroup;
	// Private methods
	this.expandWildcards=CBG_expandWildcards;
	this.addWildcardCheckboxes=CBG_addWildcardCheckboxes;
	this.addArrayCheckboxes=CBG_addArrayCheckboxes;
	this.addSingleCheckbox=CBG_addSingleCheckbox;
	this.check=CBG_check;
	}
	
CheckBoxGroup.$VERSION = 1.01;

// Set the master control checkbox name
function CBG_setControlBox(name) { this.controlBox=name; }

// Set the maximum number of checked boxes in the set, and optionally
// the message to popup when the max is reached.
function CBG_setMaxAllowed(num,msg) {
	this.maxAllowed=num;
	if (msg!=null&&msg!="") { this.maxAllowedMessage=msg; }
	}

// Set the behavior for the checkbox group master checkbox
//	All: all boxes must be checked for the master to be checked
//	Some: one or more of the boxes can be checked for the master to be checked
function CBG_setMasterBehavior(b) { this.masterBehavior = b.toLowerCase(); }

// Add checkbox wildcards to the checkboxes array
function CBG_addToGroup() {
	if (arguments.length>0) {
		for (var i=0;i<arguments.length;i++) {
			this.checkboxWildcardNames[this.checkboxWildcardNames.length]=arguments[i];
			}
		}
	}

// Expand the wildcard checkbox names given in the addToGroup method
function CBG_expandWildcards() {
	if (this.formRef==null) {alert("ERROR: No form element has been passed.  Cannot extract form name!"); return false; }
	for (var i=0; i<this.checkboxWildcardNames.length;i++) {
		var n = this.checkboxWildcardNames[i];
		var el = this.formRef[n];
		if (n.indexOf("*")!=-1) { this.addWildcardCheckboxes(n); }
		else if(CBG_nameIsArray(el)) { this.addArrayCheckboxes(n); }
		else { this.addSingleCheckbox(el); }
		}
	}


// Add checkboxes to the group which match a pattern
function CBG_addWildcardCheckboxes(name) {
	var i=name.indexOf("*");
	if ((i==0) || (i==name.length-1)) {
		var searchString= (i)?name.substring(0,name.length-1):name.substring(1,name.length);
		var els = this.formRef.elements;
		var l = els.length;
		for (var j=0;j<l;j++) {
			var currentElement = els[j];
			if (currentElement.type && currentElement.type=="checkbox" && currentElement.name) {
				var currentElementName=currentElement.name;
				var partialName = (i)?currentElementName.substring(0,searchString.length) : currentElementName.substring(currentElementName.length-searchString.length,currentElementName.length);
				if (partialName==searchString) {
					if(CBG_nameIsArray(currentElement)) this.addArrayCheckboxes(currentElement);
					else this.addSingleCheckbox(currentElement);
					}
				}
			}
		}
	}

// Add checkboxes to the group which all have the same name
function CBG_addArrayCheckboxes(name) {
	if((CBG_nameIsArray(this.formRef[name])) && (this.formRef[name].length>0)) {
		for (var i=0; i<this.formRef[name].length; i++) { this.addSingleCheckbox(this.formRef[name][i]); }
		}
	}

function CBG_addSingleCheckbox(obj) {
	if (obj != this.formRef[this.controlBox]) {
		this.checkboxNames[this.checkboxNames.length]=obj;
		this.totalBoxes++;
		if (obj.checked) {
			this.totalSelected++;
			}
		}
	}

// Runs whenever a checkbox in the group is clicked
function CBG_check(obj) {
	var checked=obj.checked;
	if (this.formRef==null) {
		this.formRef=obj.form;
		this.expandWildcards();
		if (this.controlBox==null || obj.name!=this.controlBox) {
			this.totalSelected += (checked)?-1:1;
			}
		}
	if (this.controlBox!=null&&obj.name==this.controlBox) {
		if (this.masterBehavior=="all") {
			for (i=0;i<this.checkboxNames.length;i++) { this.checkboxNames[i].checked=checked; }
			this.totalSelected=(checked)?this.checkboxNames.length:0;
			}
		else {
			if (!checked) {
				obj.checked = (this.totalSelected>0)?true:false;
				obj.blur();
				}
			}
		}
	else {
		if (this.masterBehavior=="all" && this.controlBox!=null) {
			if (!checked) {
				this.formRef[this.controlBox].checked=false;
				this.totalSelected--;
				}
			else { this.totalSelected++; }
			if (this.controlBox!=null) {
				this.formRef[this.controlBox].checked=(this.totalSelected==this.totalBoxes)?true:false;
				}
			}
		else {
			if (!obj.checked) { this.totalSelected--; }	
			else { this.totalSelected++; }
			if (this.controlBox!=null) {
				this.formRef[this.controlBox].checked=(this.totalSelected>0)?true:false;
				}
			if (this.maxAllowed!=null) {
				if (this.totalSelected>this.maxAllowed) {
					obj.checked=false;
					this.totalSelected--;
					if (this.maxAllowedMessage!=null) { alert(this.maxAllowedMessage); }
					return false;
					}
				}
			}
		}
	}

function CBG_nameIsArray(obj) {
	return ((typeof obj.type!="string")&&(obj.length>0)&&(obj[0]!=null)&&(obj[0].type=="checkbox"));
	}
