/**
 * Related for problem: https://developer.mozilla.org/ru/docs/Web/API/WindowBase64/Base64_encoding_and_decoding#Solution_.232_.E2.80.93_rewriting_atob()_and_btoa()_using_TypedArrays_and_UTF-8
 */
'use strict';

function TextEncoderLite() {
}
function TextDecoderLite() {
}

var lookup = [];
var revLookup = [];
var Arr = typeof Uint8Array !== 'undefined' ? Uint8Array : Array;

function init () {
    var i;
    var code = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
    var len = code.length;

    for (i = 0; i < len; i++) {
        lookup[i] = code[i];
    }

    for (i = 0; i < len; ++i) {
        revLookup[code.charCodeAt(i)] = i;
    }
    revLookup['-'.charCodeAt(0)] = 62;
    revLookup['_'.charCodeAt(0)] = 63;
}

init();

function toByteArray (b64) {
    var i, j, l, tmp, placeHolders, arr;
    var len = b64.length;

    if (len % 4 > 0) {
        throw new Error('Invalid string. Length must be a multiple of 4')
    }

    // the number of equal signs (place holders)
    // if there are two placeholders, than the two characters before it
    // represent one byte
    // if there is only one, then the three characters before it represent 2 bytes
    // this is just a cheap hack to not do indexOf twice
    placeHolders = b64[len - 2] === '=' ? 2 : b64[len - 1] === '=' ? 1 : 0;

    // base64 is 4/3 + up to two characters of the original data
    arr = new Arr(len * 3 / 4 - placeHolders);

    // if there are placeholders, only get up to the last complete 4 chars
    l = placeHolders > 0 ? len - 4 : len;

    var L = 0;

    for (i = 0, j = 0; i < l; i += 4, j += 3) {
        tmp = (revLookup[b64.charCodeAt(i)] << 18) | (revLookup[b64.charCodeAt(i + 1)] << 12) | (revLookup[b64.charCodeAt(i + 2)] << 6) | revLookup[b64.charCodeAt(i + 3)];
        arr[L++] = (tmp & 0xFF0000) >> 16;
        arr[L++] = (tmp & 0xFF00) >> 8;
        arr[L++] = tmp & 0xFF;
    }

    if (placeHolders === 2) {
        tmp = (revLookup[b64.charCodeAt(i)] << 2) | (revLookup[b64.charCodeAt(i + 1)] >> 4);
        arr[L++] = tmp & 0xFF;
    } else if (placeHolders === 1) {
        tmp = (revLookup[b64.charCodeAt(i)] << 10) | (revLookup[b64.charCodeAt(i + 1)] << 4) | (revLookup[b64.charCodeAt(i + 2)] >> 2);
        arr[L++] = (tmp >> 8) & 0xFF;
        arr[L++] = tmp & 0xFF;
    }

    return arr;
}

function tripletToBase64 (num) {
    return lookup[num >> 18 & 0x3F] + lookup[num >> 12 & 0x3F] + lookup[num >> 6 & 0x3F] + lookup[num & 0x3F];
}

function encodeChunk (uint8, start, end) {
    var tmp;
    var output = [];
    for (var i = start; i < end; i += 3) {
        tmp = (uint8[i] << 16) + (uint8[i + 1] << 8) + (uint8[i + 2]);
        output.push(tripletToBase64(tmp));
    }
    return output.join('');
}

function fromByteArray (uint8) {
    var tmp;
    var len = uint8.length;
    var extraBytes = len % 3; // if we have 1 byte left, pad 2 bytes
    var output = '';
    var parts = [];
    var maxChunkLength = 16383; // must be multiple of 3

    // go through the array every three bytes, we'll deal with trailing stuff later
    for (var i = 0, len2 = len - extraBytes; i < len2; i += maxChunkLength) {
        parts.push(encodeChunk(uint8, i, (i + maxChunkLength) > len2 ? len2 : (i + maxChunkLength)));
    }

    // pad the end with zeros, but make sure to not forget the extra bytes
    if (extraBytes === 1) {
        tmp = uint8[len - 1];
        output += lookup[tmp >> 2];
        output += lookup[(tmp << 4) & 0x3F];
        output += '==';
    } else if (extraBytes === 2) {
        tmp = (uint8[len - 2] << 8) + (uint8[len - 1]);
        output += lookup[tmp >> 10];
        output += lookup[(tmp >> 4) & 0x3F];
        output += lookup[(tmp << 2) & 0x3F];
        output += '=';
    }

    parts.push(output);

    return parts.join('');
}

(function () {
    'use strict';

    // Taken from https://github.com/feross/buffer/blob/master/index.js
    // Thanks Feross et al! :-)

    function utf8ToBytes (string, units) {
        units = units || Infinity;
        var codePoint;
        var length = string.length;
        var leadSurrogate = null;
        var bytes = [];
        var i = 0;

        for (; i < length; i++) {
            codePoint = string.charCodeAt(i);

            // is surrogate component
            if (codePoint > 0xD7FF && codePoint < 0xE000) {
                // last char was a lead
                if (leadSurrogate) {
                    // 2 leads in a row
                    if (codePoint < 0xDC00) {
                        if ((units -= 3) > -1) bytes.push(0xEF, 0xBF, 0xBD);
                        leadSurrogate = codePoint;
                        continue;
                    } else {
                        // valid surrogate pair
                        codePoint = leadSurrogate - 0xD800 << 10 | codePoint - 0xDC00 | 0x10000;
                        leadSurrogate = null;
                    }
                } else {
                    // no lead yet

                    if (codePoint > 0xDBFF) {
                        // unexpected trail
                        if ((units -= 3) > -1) bytes.push(0xEF, 0xBF, 0xBD);
                        continue;
                    } else if (i + 1 === length) {
                        // unpaired lead
                        if ((units -= 3) > -1) bytes.push(0xEF, 0xBF, 0xBD);
                        continue;
                    } else {
                        // valid lead
                        leadSurrogate = codePoint;
                        continue;
                    }
                }
            } else if (leadSurrogate) {
                // valid bmp char, but last char was a lead
                if ((units -= 3) > -1) bytes.push(0xEF, 0xBF, 0xBD);
                leadSurrogate = null;
            }

            // encode utf8
            if (codePoint < 0x80) {
                if ((units -= 1) < 0) break;
                bytes.push(codePoint);
            } else if (codePoint < 0x800) {
                if ((units -= 2) < 0) break;
                bytes.push(
                    codePoint >> 0x6 | 0xC0,
                    codePoint & 0x3F | 0x80
                );
            } else if (codePoint < 0x10000) {
                if ((units -= 3) < 0) break;
                bytes.push(
                    codePoint >> 0xC | 0xE0,
                    codePoint >> 0x6 & 0x3F | 0x80,
                    codePoint & 0x3F | 0x80
                );
            } else if (codePoint < 0x200000) {
                if ((units -= 4) < 0) break;
                bytes.push(
                    codePoint >> 0x12 | 0xF0,
                    codePoint >> 0xC & 0x3F | 0x80,
                    codePoint >> 0x6 & 0x3F | 0x80,
                    codePoint & 0x3F | 0x80
                );
            } else {
                throw new Error('Invalid code point');
            }
        }

        return bytes
    }

    function utf8Slice (buf, start, end) {
        var res = '';
        var tmp = '';
        end = Math.min(buf.length, end || Infinity);
        start = start || 0;

        for (var i = start; i < end; i++) {
            if (buf[i] <= 0x7F) {
                res += decodeUtf8Char(tmp) + String.fromCharCode(buf[i]);
                tmp = '';
            } else {
                tmp += '%' + buf[i].toString(16);
            }
        }

        return res + decodeUtf8Char(tmp);
    }

    function decodeUtf8Char (str) {
        try {
            return decodeURIComponent(str);
        } catch (err) {
            return String.fromCharCode(0xFFFD); // UTF 8 invalid char
        }
    }

    TextEncoderLite.prototype.encode = function (str) {
        var result;

        if ('undefined' === typeof Uint8Array) {
            result = utf8ToBytes(str);
        } else {
            result = new Uint8Array(utf8ToBytes(str));
        }

        return result;
    };

    TextDecoderLite.prototype.decode = function (bytes) {
        return utf8Slice(bytes, 0, bytes.length);
    }

}());