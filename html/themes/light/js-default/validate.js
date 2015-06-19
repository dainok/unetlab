$.validator.setDefaults({
    debug: true,
    success: "valid"
});

/*
$.validator.addMethod(
    'regexp',
    function(value, element, regexp) {
        var re = new RegExp(regexp);
        return this.optional(element) || re.test(value);
    },
    'Input not valid, must be "' + regexp + '".'
);
*/

// Validate an interger
$.validator.addMethod('integer', function(value) { 
    return /^[0-9]+$/.test(value); 
}, 'Must be interger ([0-9] chars).');

// Validate a lab name
$.validator.addMethod('lab_name', function(value) { 
    return /^[A-Za-z0-9_\-\s]+$/.test(value); 
}, 'Use only [A-Za-z0-9_- ] chars.');

// Validate a picture name
$.validator.addMethod('picture_name', function(value) { 
    return /^[A-Za-z0-9_\-\s]+$/.test(value); 
}, 'Use only [A-Za-z0-9_- ] chars.');

// Validate a node idlepc
$.validator.addMethod('node_idlepc', function(value) { 
    return /^0x[0-9a-f]+$/.test(value); 
}, 'Use a HEX value (0x[0-9a-f]+).');

// Validate folder form
function validateFolder() {
    $('.form-folder').validate({
        rules: {
            'folder[name]': {
                required: true,
                lab_name: true
            }
        }
    });
}

// Validate lab info form
function validateLabInfo() {
    $('.form-lab').validate({
        rules: {
            'lab[name]': {
                required: true,
                lab_name: true
            },
            'lab[version]': {
                required: false,
                integer: true
            }
        }
    });
}

// Validate lab network form
function validateLabNetwork() {
    $('.form-network').validate({
        rules: {
            'network[count]': {
                required: true,
                integer: true
            },
            'network[name]': {
                required: true
            }
        }
    });
}

// Validate lab node form
function validateLabNode() {
    $('.form-node').validate({
        rules: {
            'node[count]': {
                required: true,
                integer: true
            },
            'node[name]': {
                required: true
            },
            'node[cpu]': {
                required: true,
                integer: true
            },
            'node[idlepc]': {
                required: true,
                node_idlepc: true
            },
            'node[ram]': {
                required: true,
                integer: true
            },
            'node[nvram]': {
                required: true,
                integer: true
            },
            'node[ethernet]': {
                required: true,
                integer: true
            },
            'node[serial]': {
                required: true,
                integer: true
            },
            'node[delay]': {
                required: true,
                integer: true
            }
        }
    });
}

// Validate lab picture form
function validateLabPicture() {
    $('.form-picture').validate({
        rules: {
            'picture[name]': {
                required: true
            }
        }
    });
}
