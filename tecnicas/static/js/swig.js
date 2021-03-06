!function() {
    var str = "{{ a }}",
        splitter;
    if (str.split(/(\{\{.*?\}\})/).length === 0) {
        splitter = function(str, separator, limit) {
            if (Object.prototype.toString.call(separator) !== "[object RegExp]") {
                return splitter._nativeSplit.call(str, separator, limit)
            }
            var output = [],
                lastLastIndex = 0,
                flags = (separator.ignoreCase ? "i" : "") + (separator.multiline ? "m" : "") + (separator.sticky ? "y" : ""),
                separator2, match, lastIndex, lastLength;
            separator = RegExp(separator.source, flags + "g");
            str = str.toString();
            if (!splitter._compliantExecNpcg) {
                separator2 = RegExp("^" + separator.source + "$(?!\\s)", flags)
            }
            if (limit === undefined || limit < 0) {
                limit = Infinity
            } else {
                limit = Math.floor(+limit);
                if (!limit) {
                    return []
                }
            }
            function fixExec() {
                var i = 1;
                for (i; i < arguments.length - 2; i += 1) {
                    if (arguments[i] === undefined) {
                        match[i] = undefined
                    }
                }
            }
            match = separator.exec(str);
            while (match) {
                lastIndex = match.index + match[0].length;
                if (lastIndex > lastLastIndex) {
                    output.push(str.slice(lastLastIndex, match.index));
                    if (!splitter._compliantExecNpcg && match.length > 1) {
                        match[0].replace(separator2, fixExec)
                    }
                    if (match.length > 1 && match.index < str.length) {
                        Array.prototype.push.apply(output, match.slice(1))
                    }
                    lastLength = match[0].length;
                    lastLastIndex = lastIndex;
                    if (output.length >= limit) {
                        break
                    }
                }
                if (separator.lastIndex === match.index) {
                    separator.lastIndex += 1
                }
                match = separator.exec(str)
            }
            if (lastLastIndex === str.length) {
                if (lastLength || !separator.test("")) {
                    output.push("")
                }
            } else {
                output.push(str.slice(lastLastIndex))
            }
            return output.length > limit ? output.slice(0, limit) : output
        };
        splitter._compliantExecNpcg = /()??/.exec("")[1] === undefined;
        splitter._nativeSplit = String.prototype.split;
        String.prototype.split = function(separator, limit) {
            return splitter(this, separator, limit)
        }
    }
}();
swig = function() {
    var swig = {}, dateformat = {}, filters = {}, helpers = {}, parser = {}, tags = {};
    ! function() {
        var root = this;
        var previousUnderscore = root._;
        var breaker = {};
        var ArrayProto = Array.prototype,
            ObjProto = Object.prototype,
            FuncProto = Function.prototype;
        var push = ArrayProto.push,
            slice = ArrayProto.slice,
            concat = ArrayProto.concat,
            toString = ObjProto.toString,
            hasOwnProperty = ObjProto.hasOwnProperty;
        var nativeForEach = ArrayProto.forEach,
            nativeMap = ArrayProto.map,
            nativeReduce = ArrayProto.reduce,
            nativeReduceRight = ArrayProto.reduceRight,
            nativeFilter = ArrayProto.filter,
            nativeEvery = ArrayProto.every,
            nativeSome = ArrayProto.some,
            nativeIndexOf = ArrayProto.indexOf,
            nativeLastIndexOf = ArrayProto.lastIndexOf,
            nativeIsArray = Array.isArray,
            nativeKeys = Object.keys,
            nativeBind = FuncProto.bind;
        var _ = function(obj) {
            if (obj instanceof _) return obj;
            if (!(this instanceof _)) return new _(obj);
            this._wrapped = obj
        };
        if (typeof exports !== "undefined") {
            if (typeof module !== "undefined" && module.exports) {
                exports = module.exports = _
            }
            exports._ = _
        } else {
            root._ = _
        }
        _.VERSION = "1.4.4";
        var each = _.each = _.forEach = function(obj, iterator, context) {
            if (obj == null) return;
            if (nativeForEach && obj.forEach === nativeForEach) {
                obj.forEach(iterator, context)
            } else if (obj.length === +obj.length) {
                for (var i = 0, l = obj.length; i < l; i++) {
                    if (iterator.call(context, obj[i], i, obj) === breaker) return
                }
            } else {
                for (var key in obj) {
                    if (_.has(obj, key)) {
                        if (iterator.call(context, obj[key], key, obj) === breaker) return
                    }
                }
            }
        };
        _.map = _.collect = function(obj, iterator, context) {
            var results = [];
            if (obj == null) return results;
            if (nativeMap && obj.map === nativeMap) return obj.map(iterator, context);
            each(obj, function(value, index, list) {
                results[results.length] = iterator.call(context, value, index, list)
            });
            return results
        };
        var reduceError = "Reduce of empty array with no initial value";
        _.reduce = _.foldl = _.inject = function(obj, iterator, memo, context) {
            var initial = arguments.length > 2;
            if (obj == null) obj = [];
            if (nativeReduce && obj.reduce === nativeReduce) {
                if (context) iterator = _.bind(iterator, context);
                return initial ? obj.reduce(iterator, memo) : obj.reduce(iterator)
            }
            each(obj, function(value, index, list) {
                if (!initial) {
                    memo = value;
                    initial = true
                } else {
                    memo = iterator.call(context, memo, value, index, list)
                }
            });
            if (!initial) throw new TypeError(reduceError);
            return memo
        };
        _.reduceRight = _.foldr = function(obj, iterator, memo, context) {
            var initial = arguments.length > 2;
            if (obj == null) obj = [];
            if (nativeReduceRight && obj.reduceRight === nativeReduceRight) {
                if (context) iterator = _.bind(iterator, context);
                return initial ? obj.reduceRight(iterator, memo) : obj.reduceRight(iterator)
            }
            var length = obj.length;
            if (length !== +length) {
                var keys = _.keys(obj);
                length = keys.length
            }
            each(obj, function(value, index, list) {
                index = keys ? keys[--length] : --length;
                if (!initial) {
                    memo = obj[index];
                    initial = true
                } else {
                    memo = iterator.call(context, memo, obj[index], index, list)
                }
            });
            if (!initial) throw new TypeError(reduceError);
            return memo
        };
        _.find = _.detect = function(obj, iterator, context) {
            var result;
            any(obj, function(value, index, list) {
                if (iterator.call(context, value, index, list)) {
                    result = value;
                    return true
                }
            });
            return result
        };
        _.filter = _.select = function(obj, iterator, context) {
            var results = [];
            if (obj == null) return results;
            if (nativeFilter && obj.filter === nativeFilter) return obj.filter(iterator, context);
            each(obj, function(value, index, list) {
                if (iterator.call(context, value, index, list)) results[results.length] = value
            });
            return results
        };
        _.reject = function(obj, iterator, context) {
            return _.filter(obj, function(value, index, list) {
                return !iterator.call(context, value, index, list)
            }, context)
        };
        _.every = _.all = function(obj, iterator, context) {
            iterator || (iterator = _.identity);
            var result = true;
            if (obj == null) return result;
            if (nativeEvery && obj.every === nativeEvery) return obj.every(iterator, context);
            each(obj, function(value, index, list) {
                if (!(result = result && iterator.call(context, value, index, list))) return breaker
            });
            return !!result
        };
        var any = _.some = _.any = function(obj, iterator, context) {
            iterator || (iterator = _.identity);
            var result = false;
            if (obj == null) return result;
            if (nativeSome && obj.some === nativeSome) return obj.some(iterator, context);
            each(obj, function(value, index, list) {
                if (result || (result = iterator.call(context, value, index, list))) return breaker
            });
            return !!result
        };
        _.contains = _.include = function(obj, target) {
            if (obj == null) return false;
            if (nativeIndexOf && obj.indexOf === nativeIndexOf) return obj.indexOf(target) != -1;
            return any(obj, function(value) {
                return value === target
            })
        };
        _.invoke = function(obj, method) {
            var args = slice.call(arguments, 2);
            var isFunc = _.isFunction(method);
            return _.map(obj, function(value) {
                return (isFunc ? method : value[method]).apply(value, args)
            })
        };
        _.pluck = function(obj, key) {
            return _.map(obj, function(value) {
                return value[key]
            })
        };
        _.where = function(obj, attrs, first) {
            if (_.isEmpty(attrs)) return first ? null : [];
            return _[first ? "find" : "filter"](obj, function(value) {
                for (var key in attrs) {
                    if (attrs[key] !== value[key]) return false
                }
                return true
            })
        };
        _.findWhere = function(obj, attrs) {
            return _.where(obj, attrs, true)
        };
        _.max = function(obj, iterator, context) {
            if (!iterator && _.isArray(obj) && obj[0] === +obj[0] && obj.length < 65535) {
                return Math.max.apply(Math, obj)
            }
            if (!iterator && _.isEmpty(obj)) return -Infinity;
            var result = {
                computed: -Infinity,
                value: -Infinity
            };
            each(obj, function(value, index, list) {
                var computed = iterator ? iterator.call(context, value, index, list) : value;
                computed >= result.computed && (result = {
                    value: value,
                    computed: computed
                })
            });
            return result.value
        };
        _.min = function(obj, iterator, context) {
            if (!iterator && _.isArray(obj) && obj[0] === +obj[0] && obj.length < 65535) {
                return Math.min.apply(Math, obj)
            }
            if (!iterator && _.isEmpty(obj)) return Infinity;
            var result = {
                computed: Infinity,
                value: Infinity
            };
            each(obj, function(value, index, list) {
                var computed = iterator ? iterator.call(context, value, index, list) : value;
                computed < result.computed && (result = {
                    value: value,
                    computed: computed
                })
            });
            return result.value
        };
        _.shuffle = function(obj) {
            var rand;
            var index = 0;
            var shuffled = [];
            each(obj, function(value) {
                rand = _.random(index++);
                shuffled[index - 1] = shuffled[rand];
                shuffled[rand] = value
            });
            return shuffled
        };
        var lookupIterator = function(value) {
            return _.isFunction(value) ? value : function(obj) {
                return obj[value]
            }
        };
        _.sortBy = function(obj, value, context) {
            var iterator = lookupIterator(value);
            return _.pluck(_.map(obj, function(value, index, list) {
                return {
                    value: value,
                    index: index,
                    criteria: iterator.call(context, value, index, list)
                }
            }).sort(function(left, right) {
                var a = left.criteria;
                var b = right.criteria;
                if (a !== b) {
                    if (a > b || a === void 0) return 1;
                    if (a < b || b === void 0) return -1
                }
                return left.index < right.index ? -1 : 1
            }), "value")
        };
        var group = function(obj, value, context, behavior) {
            var result = {};
            var iterator = lookupIterator(value || _.identity);
            each(obj, function(value, index) {
                var key = iterator.call(context, value, index, obj);
                behavior(result, key, value)
            });
            return result
        };
        _.groupBy = function(obj, value, context) {
            return group(obj, value, context, function(result, key, value) {
                (_.has(result, key) ? result[key] : result[key] = []).push(value)
            })
        };
        _.countBy = function(obj, value, context) {
            return group(obj, value, context, function(result, key) {
                if (!_.has(result, key)) result[key] = 0;
                result[key]++
            })
        };
        _.sortedIndex = function(array, obj, iterator, context) {
            iterator = iterator == null ? _.identity : lookupIterator(iterator);
            var value = iterator.call(context, obj);
            var low = 0,
                high = array.length;
            while (low < high) {
                var mid = low + high >>> 1;
                iterator.call(context, array[mid]) < value ? low = mid + 1 : high = mid
            }
            return low
        };
        _.toArray = function(obj) {
            if (!obj) return [];
            if (_.isArray(obj)) return slice.call(obj);
            if (obj.length === +obj.length) return _.map(obj, _.identity);
            return _.values(obj)
        };
        _.size = function(obj) {
            if (obj == null) return 0;
            return obj.length === +obj.length ? obj.length : _.keys(obj).length
        };
        _.first = _.head = _.take = function(array, n, guard) {
            if (array == null) return void 0;
            return n != null && !guard ? slice.call(array, 0, n) : array[0]
        };
        _.initial = function(array, n, guard) {
            return slice.call(array, 0, array.length - (n == null || guard ? 1 : n))
        };
        _.last = function(array, n, guard) {
            if (array == null) return void 0;
            if (n != null && !guard) {
                return slice.call(array, Math.max(array.length - n, 0))
            } else {
                return array[array.length - 1]
            }
        };
        _.rest = _.tail = _.drop = function(array, n, guard) {
            return slice.call(array, n == null || guard ? 1 : n)
        };
        _.compact = function(array) {
            return _.filter(array, _.identity)
        };
        var flatten = function(input, shallow, output) {
            each(input, function(value) {
                if (_.isArray(value)) {
                    shallow ? push.apply(output, value) : flatten(value, shallow, output)
                } else {
                    output.push(value)
                }
            });
            return output
        };
        _.flatten = function(array, shallow) {
            return flatten(array, shallow, [])
        };
        _.without = function(array) {
            return _.difference(array, slice.call(arguments, 1))
        };
        _.uniq = _.unique = function(array, isSorted, iterator, context) {
            if (_.isFunction(isSorted)) {
                context = iterator;
                iterator = isSorted;
                isSorted = false
            }
            var initial = iterator ? _.map(array, iterator, context) : array;
            var results = [];
            var seen = [];
            each(initial, function(value, index) {
                if (isSorted ? !index || seen[seen.length - 1] !== value : !_.contains(seen, value)) {
                    seen.push(value);
                    results.push(array[index])
                }
            });
            return results
        };
        _.union = function() {
            return _.uniq(concat.apply(ArrayProto, arguments))
        };
        _.intersection = function(array) {
            var rest = slice.call(arguments, 1);
            return _.filter(_.uniq(array), function(item) {
                return _.every(rest, function(other) {
                    return _.indexOf(other, item) >= 0
                })
            })
        };
        _.difference = function(array) {
            var rest = concat.apply(ArrayProto, slice.call(arguments, 1));
            return _.filter(array, function(value) {
                return !_.contains(rest, value)
            })
        };
        _.zip = function() {
            var args = slice.call(arguments);
            var length = _.max(_.pluck(args, "length"));
            var results = new Array(length);
            for (var i = 0; i < length; i++) {
                results[i] = _.pluck(args, "" + i)
            }
            return results
        };
        _.object = function(list, values) {
            if (list == null) return {};
            var result = {};
            for (var i = 0, l = list.length; i < l; i++) {
                if (values) {
                    result[list[i]] = values[i]
                } else {
                    result[list[i][0]] = list[i][1]
                }
            }
            return result
        };
        _.indexOf = function(array, item, isSorted) {
            if (array == null) return -1;
            var i = 0,
                l = array.length;
            if (isSorted) {
                if (typeof isSorted == "number") {
                    i = isSorted < 0 ? Math.max(0, l + isSorted) : isSorted
                } else {
                    i = _.sortedIndex(array, item);
                    return array[i] === item ? i : -1
                }
            }
            if (nativeIndexOf && array.indexOf === nativeIndexOf) return array.indexOf(item, isSorted);
            for (; i < l; i++) if (array[i] === item) return i;
            return -1
        };
        _.lastIndexOf = function(array, item, from) {
            if (array == null) return -1;
            var hasIndex = from != null;
            if (nativeLastIndexOf && array.lastIndexOf === nativeLastIndexOf) {
                return hasIndex ? array.lastIndexOf(item, from) : array.lastIndexOf(item)
            }
            var i = hasIndex ? from : array.length;
            while (i--) if (array[i] === item) return i;
            return -1
        };
        _.range = function(start, stop, step) {
            if (arguments.length <= 1) {
                stop = start || 0;
                start = 0
            }
            step = arguments[2] || 1;
            var len = Math.max(Math.ceil((stop - start) / step), 0);
            var idx = 0;
            var range = new Array(len);
            while (idx < len) {
                range[idx++] = start;
                start += step
            }
            return range
        };
        _.bind = function(func, context) {
            if (func.bind === nativeBind && nativeBind) return nativeBind.apply(func, slice.call(arguments, 1));
            var args = slice.call(arguments, 2);
            return function() {
                return func.apply(context, args.concat(slice.call(arguments)))
            }
        };
        _.partial = function(func) {
            var args = slice.call(arguments, 1);
            return function() {
                return func.apply(this, args.concat(slice.call(arguments)))
            }
        };
        _.bindAll = function(obj) {
            var funcs = slice.call(arguments, 1);
            if (funcs.length === 0) funcs = _.functions(obj);
            each(funcs, function(f) {
                obj[f] = _.bind(obj[f], obj)
            });
            return obj
        };
        _.memoize = function(func, hasher) {
            var memo = {};
            hasher || (hasher = _.identity);
            return function() {
                var key = hasher.apply(this, arguments);
                return _.has(memo, key) ? memo[key] : memo[key] = func.apply(this, arguments)
            }
        };
        _.delay = function(func, wait) {
            var args = slice.call(arguments, 2);
            return setTimeout(function() {
                return func.apply(null, args)
            }, wait)
        };
        _.defer = function(func) {
            return _.delay.apply(_, [func, 1].concat(slice.call(arguments, 1)))
        };
        _.throttle = function(func, wait) {
            var context, args, timeout, result;
            var previous = 0;
            var later = function() {
                previous = new Date;
                timeout = null;
                result = func.apply(context, args)
            };
            return function() {
                var now = new Date;
                var remaining = wait - (now - previous);
                context = this;
                args = arguments;
                if (remaining <= 0) {
                    clearTimeout(timeout);
                    timeout = null;
                    previous = now;
                    result = func.apply(context, args)
                } else if (!timeout) {
                    timeout = setTimeout(later, remaining)
                }
                return result
            }
        };
        _.debounce = function(func, wait, immediate) {
            var timeout, result;
            return function() {
                var context = this,
                    args = arguments;
                var later = function() {
                    timeout = null;
                    if (!immediate) result = func.apply(context, args)
                };
                var callNow = immediate && !timeout;
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
                if (callNow) result = func.apply(context, args);
                return result
            }
        };
        _.once = function(func) {
            var ran = false,
                memo;
            return function() {
                if (ran) return memo;
                ran = true;
                memo = func.apply(this, arguments);
                func = null;
                return memo
            }
        };
        _.wrap = function(func, wrapper) {
            return function() {
                var args = [func];
                push.apply(args, arguments);
                return wrapper.apply(this, args)
            }
        };
        _.compose = function() {
            var funcs = arguments;
            return function() {
                var args = arguments;
                for (var i = funcs.length - 1; i >= 0; i--) {
                    args = [funcs[i].apply(this, args)]
                }
                return args[0]
            }
        };
        _.after = function(times, func) {
            if (times <= 0) return func();
            return function() {
                if (--times < 1) {
                    return func.apply(this, arguments)
                }
            }
        };
        _.keys = nativeKeys || function(obj) {
            if (obj !== Object(obj)) throw new TypeError("Invalid object");
            var keys = [];
            for (var key in obj) if (_.has(obj, key)) keys[keys.length] = key;
            return keys
        };
        _.values = function(obj) {
            var values = [];
            for (var key in obj) if (_.has(obj, key)) values.push(obj[key]);
            return values
        };
        _.pairs = function(obj) {
            var pairs = [];
            for (var key in obj) if (_.has(obj, key)) pairs.push([key, obj[key]]);
            return pairs
        };
        _.invert = function(obj) {
            var result = {};
            for (var key in obj) if (_.has(obj, key)) result[obj[key]] = key;
            return result
        };
        _.functions = _.methods = function(obj) {
            var names = [];
            for (var key in obj) {
                if (_.isFunction(obj[key])) names.push(key)
            }
            return names.sort()
        };
        _.extend = function(obj) {
            each(slice.call(arguments, 1), function(source) {
                if (source) {
                    for (var prop in source) {
                        obj[prop] = source[prop]
                    }
                }
            });
            return obj
        };
        _.pick = function(obj) {
            var copy = {};
            var keys = concat.apply(ArrayProto, slice.call(arguments, 1));
            each(keys, function(key) {
                if (key in obj) copy[key] = obj[key]
            });
            return copy
        };
        _.omit = function(obj) {
            var copy = {};
            var keys = concat.apply(ArrayProto, slice.call(arguments, 1));
            for (var key in obj) {
                if (!_.contains(keys, key)) copy[key] = obj[key]
            }
            return copy
        };
        _.defaults = function(obj) {
            each(slice.call(arguments, 1), function(source) {
                if (source) {
                    for (var prop in source) {
                        if (obj[prop] == null) obj[prop] = source[prop]
                    }
                }
            });
            return obj
        };
        _.clone = function(obj) {
            if (!_.isObject(obj)) return obj;
            return _.isArray(obj) ? obj.slice() : _.extend({}, obj)
        };
        _.tap = function(obj, interceptor) {
            interceptor(obj);
            return obj
        };
        var eq = function(a, b, aStack, bStack) {
            if (a === b) return a !== 0 || 1 / a == 1 / b;
            if (a == null || b == null) return a === b;
            if (a instanceof _) a = a._wrapped;
            if (b instanceof _) b = b._wrapped;
            var className = toString.call(a);
            if (className != toString.call(b)) return false;
            switch (className) {
                case "[object String]":
                    return a == String(b);
                case "[object Number]":
                    return a != +a ? b != +b : a == 0 ? 1 / a == 1 / b : a == +b;
                case "[object Date]":
                case "[object Boolean]":
                    return +a == +b;
                case "[object RegExp]":
                    return a.source == b.source && a.global == b.global && a.multiline == b.multiline && a.ignoreCase == b.ignoreCase
            }
            if (typeof a != "object" || typeof b != "object") return false;
            var length = aStack.length;
            while (length--) {
                if (aStack[length] == a) return bStack[length] == b
            }
            aStack.push(a);
            bStack.push(b);
            var size = 0,
                result = true;
            if (className == "[object Array]") {
                size = a.length;
                result = size == b.length;
                if (result) {
                    while (size--) {
                        if (!(result = eq(a[size], b[size], aStack, bStack))) break
                    }
                }
            } else {
                var aCtor = a.constructor,
                    bCtor = b.constructor;
                if (aCtor !== bCtor && !(_.isFunction(aCtor) && aCtor instanceof aCtor && _.isFunction(bCtor) && bCtor instanceof bCtor)) {
                    return false
                }
                for (var key in a) {
                    if (_.has(a, key)) {
                        size++;
                        if (!(result = _.has(b, key) && eq(a[key], b[key], aStack, bStack))) break
                    }
                }
                if (result) {
                    for (key in b) {
                        if (_.has(b, key) && !size--) break
                    }
                    result = !size
                }
            }
            aStack.pop();
            bStack.pop();
            return result
        };
        _.isEqual = function(a, b) {
            return eq(a, b, [], [])
        };
        _.isEmpty = function(obj) {
            if (obj == null) return true;
            if (_.isArray(obj) || _.isString(obj)) return obj.length === 0;
            for (var key in obj) if (_.has(obj, key)) return false;
            return true
        };
        _.isElement = function(obj) {
            return !!(obj && obj.nodeType === 1)
        };
        _.isArray = nativeIsArray || function(obj) {
            return toString.call(obj) == "[object Array]"
        };
        _.isObject = function(obj) {
            return obj === Object(obj)
        };
        each(["Arguments", "Function", "String", "Number", "Date", "RegExp"], function(name) {
            _["is" + name] = function(obj) {
                return toString.call(obj) == "[object " + name + "]"
            }
        });
        if (!_.isArguments(arguments)) {
            _.isArguments = function(obj) {
                return !!(obj && _.has(obj, "callee"))
            }
        }
        if (typeof / . / !== "function") {
            _.isFunction = function(obj) {
                return typeof obj === "function"
            }
        }
        _.isFinite = function(obj) {
            return isFinite(obj) && !isNaN(parseFloat(obj))
        };
        _.isNaN = function(obj) {
            return _.isNumber(obj) && obj != +obj
        };
        _.isBoolean = function(obj) {
            return obj === true || obj === false || toString.call(obj) == "[object Boolean]"
        };
        _.isNull = function(obj) {
            return obj === null
        };
        _.isUndefined = function(obj) {
            return obj === void 0
        };
        _.has = function(obj, key) {
            return hasOwnProperty.call(obj, key)
        };
        _.noConflict = function() {
            root._ = previousUnderscore;
            return this
        };
        _.identity = function(value) {
            return value
        };
        _.times = function(n, iterator, context) {
            var accum = Array(n);
            for (var i = 0; i < n; i++) accum[i] = iterator.call(context, i);
            return accum
        };
        _.random = function(min, max) {
            if (max == null) {
                max = min;
                min = 0
            }
            return min + Math.floor(Math.random() * (max - min + 1))
        };
        var entityMap = {
            escape: {
                "&": "&",
                "<": "<",
                ">": ">",
                '"': '"',
                "'": "'",
                "/": "/"
            }
        };
        entityMap.unescape = _.invert(entityMap.escape);
        var entityRegexes = {
            escape: new RegExp("[" + _.keys(entityMap.escape).join("") + "]", "g"),
            unescape: new RegExp("(" + _.keys(entityMap.unescape).join("|") + ")", "g")
        };
        _.each(["escape", "unescape"], function(method) {
            _[method] = function(string) {
                if (string == null) return "";
                return ("" + string).replace(entityRegexes[method], function(match) {
                    return entityMap[method][match]
                })
            }
        });
        _.result = function(object, property) {
            if (object == null) return null;
            var value = object[property];
            return _.isFunction(value) ? value.call(object) : value
        };
        _.mixin = function(obj) {
            each(_.functions(obj), function(name) {
                var func = _[name] = obj[name];
                _.prototype[name] = function() {
                    var args = [this._wrapped];
                    push.apply(args, arguments);
                    return result.call(this, func.apply(_, args))
                }
            })
        };
        var idCounter = 0;
        _.uniqueId = function(prefix) {
            var id = ++idCounter + "";
            return prefix ? prefix + id : id
        };
        _.templateSettings = {
            evaluate: /<%([\s\S]+?)%>/g,
            interpolate: /<%=([\s\S]+?)%>/g,
            escape: /<%-([\s\S]+?)%>/g
        };
        var noMatch = /(.)^/;
        var escapes = {
            "'": "'",
            "\\": "\\",
            "\r": "r",
            "\n": "n",
            "	": "t",
            "\u2028": "u2028",
            "\u2029": "u2029"
        };
        var escaper = /\\|'|\r|\n|\t|\u2028|\u2029/g;
        _.template = function(text, data, settings) {
            var render;
            settings = _.defaults({}, settings, _.templateSettings);
            var matcher = new RegExp([(settings.escape || noMatch).source, (settings.interpolate || noMatch).source, (settings.evaluate || noMatch).source].join("|") + "|$", "g");
            var index = 0;
            var source = "__p+='";
            text.replace(matcher, function(match, escape, interpolate, evaluate, offset) {
                source += text.slice(index, offset).replace(escaper, function(match) {
                    return "\\" + escapes[match]
                });
                if (escape) {
                    source += "'+\n((__t=(" + escape + "))==null?'':_.escape(__t))+\n'"
                }
                if (interpolate) {
                    source += "'+\n((__t=(" + interpolate + "))==null?'':__t)+\n'"
                }
                if (evaluate) {
                    source += "';\n" + evaluate + "\n__p+='"
                }
                index = offset + match.length;
                return match
            });
            source += "';\n";
            if (!settings.variable) source = "with(obj||{}){\n" + source + "}\n";
            source = "var __t,__p='',__j=Array.prototype.join," + "print=function(){__p+=__j.call(arguments,'');};\n" + source + "return __p;\n";
            try {
                render = new Function(settings.variable || "obj", "_", source)
            } catch (e) {
                e.source = source;
                throw e
            }
            if (data) return render(data, _);
            var template = function(data) {
                return render.call(this, data, _)
            };
            template.source = "function(" + (settings.variable || "obj") + "){\n" + source + "}";
            return template
        };
        _.chain = function(obj) {
            return _(obj).chain()
        };
        var result = function(obj) {
            return this._chain ? _(obj).chain() : obj
        };
        _.mixin(_);
        each(["pop", "push", "reverse", "shift", "sort", "splice", "unshift"], function(name) {
            var method = ArrayProto[name];
            _.prototype[name] = function() {
                var obj = this._wrapped;
                method.apply(obj, arguments);
                if ((name == "shift" || name == "splice") && obj.length === 0) delete obj[0];
                return result.call(this, obj)
            }
        });
        each(["concat", "join", "slice"], function(name) {
            var method = ArrayProto[name];
            _.prototype[name] = function() {
                return result.call(this, method.apply(this._wrapped, arguments))
            }
        });
        _.extend(_.prototype, {
            chain: function() {
                this._chain = true;
                return this
            },
            value: function() {
                return this._wrapped
            }
        })
    }.call(this);
    ! function(exports) {
        var config = {
            allowErrors: false,
            autoescape: true,
            cache: true,
            encoding: "utf8",
            filters: filters,
            root: "/",
            tags: tags,
            extensions: {},
            tzOffset: 0
        }, _config = _.extend({}, config),
            CACHE = {};
        exports.init = function(options) {
            CACHE = {};
            _config = _.extend({}, config, options);
            _config.filters = _.extend(filters, options.filters);
            _config.tags = _.extend(tags, options.tags);
            dateformat.defaultTZOffset = _config.tzOffset
        };

        function TemplateError(error) {
            return {
                render: function() {
                    return "<pre>" + error.stack + "</pre>"
                }
            }
        }
        function createRenderFunc(code) {
            return new Function("_context", "_parents", "_filters", "_", "_ext", ["_parents = _parents ? _parents.slice() : [];", "_context = _context || {};", "var j = _parents.length,", '  _output = "",', "  _this = this;", "while (j--) {", "   if (_parents[j] === this.id) {", '     return "Circular import of template " + this.id + " in " + _parents[_parents.length-1];', "   }", "}", "_parents.push(this.id);", code, "return _output;"].join(""))
        }
        function createTemplate(data, id) {
            var template = {
                compileFile: exports.compileFile,
                blocks: {},
                type: parser.TEMPLATE,
                id: id
            }, tokens, code, render;
            if (_config.allowErrors) {
                tokens = parser.parse.call(template, data, _config.tags, _config.autoescape)
            } else {
                try {
                    tokens = parser.parse.call(template, data, _config.tags, _config.autoescape)
                } catch (e) {
                    return new TemplateError(e)
                }
            }
            template.tokens = tokens;
            code = parser.compile.call(template);
            if (code !== false) {
                render = createRenderFunc(code)
            } else {
                render = function(_context, _parents, _filters, _, _ext) {
                    template.tokens = tokens;
                    code = parser.compile.call(template, "", _context);
                    var fn = createRenderFunc(code);
                    return fn.call(this, _context, _parents, _filters, _, _ext)
                }
            }
            template.render = function(context, parents) {
                if (_config.allowErrors) {
                    return render.call(this, context, parents, _config.filters, _, _config.extensions)
                }
                try {
                    return render.call(this, context, parents, _config.filters, _, _config.extensions)
                } catch (e) {
                    return new TemplateError(e)
                }
            };
            return template
        }
        function getTemplate(source, options) {
            var key = options.filename || source;
            if (_config.cache || options.cache) {
                if (!CACHE.hasOwnProperty(key)) {
                    CACHE[key] = createTemplate(source, key)
                }
                return CACHE[key]
            }
            return createTemplate(source, key)
        }
        exports.compileFile = function(filepath, forceAllowErrors) {
            var tpl, get;
            if (_config.cache && CACHE.hasOwnProperty(filepath)) {
                return CACHE[filepath]
            }
            if (typeof window !== "undefined") {
                throw new TemplateError({
                    stack: "You must pre-compile all templates in-browser. Use `swig.compile(template);`."
                })
            }
            get = function() {
                var excp, getSingle, c;
                getSingle = function(prefix) {
                    var file = /^\//.test(filepath) || /^.:/.test(filepath) ? filepath : prefix + "/" + filepath,
                        data;
                    try {
                        data = fs.readFileSync(file, config.encoding);
                        tpl = getTemplate(data, {
                            filename: filepath
                        })
                    } catch (e) {
                        excp = e
                    }
                };
                if (typeof _config.root === "string") {
                    getSingle(_config.root)
                }
                if (_config.root instanceof Array) {
                    c = 0;
                    while (tpl === undefined && c < _config.root.length) {
                        getSingle(_config.root[c]);
                        c = c + 1
                    }
                }
                if (tpl === undefined) {
                    throw excp
                }
            };
            if (_config.allowErrors || forceAllowErrors) {
                get()
            } else {
                try {
                    get()
                } catch (error) {
                    tpl = new TemplateError(error)
                }
            }
            return tpl
        };
        exports.compile = function(source, options) {
            var tmpl = getTemplate(source, options || {});
            return function(source, options) {
                return tmpl.render(source, options)
            }
        }
    }(swig);
    ! function(exports) {
        var KEYWORDS = /^(Array|ArrayBuffer|Boolean|Date|Error|eval|EvalError|Function|Infinity|Iterator|JSON|Math|Namespace|NaN|Number|Object|QName|RangeError|ReferenceError|RegExp|StopIteration|String|SyntaxError|TypeError|undefined|uneval|URIError|XML|XMLList|break|case|catch|continue|debugger|default|delete|do|else|finally|for|function|if|in|instanceof|new|return|switch|this|throw|try|typeof|var|void|while|with)(?=(\.|$))/;
        exports.isStringLiteral = function(string) {
            if (typeof string !== "string") {
                return false
            }
            var first = string.substring(0, 1),
                last = string.charAt(string.length - 1, 1),
                teststr;
            if (first === last && (first === "'" || first === '"')) {
                teststr = string.substr(1, string.length - 2).split("").reverse().join("");
                if (first === "'" && /'(?!\\)/.test(teststr) || last === '"' && /"(?!\\)/.test(teststr)) {
                    throw new Error("Invalid string literal. Unescaped quote (" + string[0] + ") found.")
                }
                return true
            }
            return false
        };
        exports.isLiteral = function(string) {
            var literal = false;
            if (/^\d+([.]\d+)?$/.test(string)) {
                literal = true
            } else if (exports.isStringLiteral(string)) {
                literal = true
            }
            return literal
        };
        exports.isValidName = function(string) {
            return typeof string === "string" && string.substr(0, 2) !== "__" && /^([$A-Za-z_]+[$A-Za-z_0-9]*)(\.?([$A-Za-z_]+[$A-Za-z_0-9]*))*$/.test(string) && !KEYWORDS.test(string)
        };
        exports.isValidShortName = function(string) {
            return string.substr(0, 2) !== "__" && /^[$A-Za-z_]+[$A-Za-z_0-9]*$/.test(string) && !KEYWORDS.test(string)
        };
        exports.isValidBlockName = function(string) {
            return /^[A-Za-z]+[A-Za-z_0-9]*$/.test(string)
        };

        function stripWhitespace(input) {
            return input.replace(/^\s+|\s+$/g, "")
        }
        exports.stripWhitespace = stripWhitespace;

        function filterVariablePath(props) {
            var filtered = [],
                literal = "",
                i = 0;
            for (i; i < props.length; i += 1) {
                if (props[i] && props[i].charAt(0) !== props[i].charAt(props[i].length - 1) && (props[i].indexOf('"') === 0 || props[i].indexOf("'") === 0)) {
                    literal = props[i];
                    continue
                }
                if (props[i] === "." && literal) {
                    literal += ".";
                    continue
                }
                if (props[i].indexOf('"') === props[i].length - 1 || props[i].indexOf("'") === props[i].length - 1) {
                    literal += props[i];
                    filtered.push(literal);
                    literal = ""
                } else {
                    filtered.push(props[i])
                }
            }
            return _.compact(filtered)
        }
        function check(variable, context) {
            if (_.isArray(variable)) {
                return "(true)"
            }
            variable = variable.replace(/^this/, "_this.__currentContext");
            if (exports.isLiteral(variable)) {
                return "(true)"
            }
            var props = variable.split(/(\.|\[|\])/),
                chain = "",
                output = [],
                inArr = false,
                prevDot = false;
            if (typeof context === "string" && context.length) {
                props.unshift(context)
            }
            props = _.reject(props, function(val) {
                return val === ""
            });
            props = filterVariablePath(props);
            _.each(props, function(prop) {
                if (prop === ".") {
                    prevDot = true;
                    return
                }
                if (prop === "[") {
                    inArr = true;
                    return
                }
                if (prop === "]") {
                    inArr = false;
                    return
                }
                if (!chain) {
                    chain = prop
                } else if (inArr) {
                    if (!exports.isStringLiteral(prop)) {
                        if (prevDot) {
                            output[output.length - 1] = _.last(output).replace(/\] !== "undefined"$/, "_" + prop + '] !== "undefined"');
                            chain = chain.replace(/\]$/, "_" + prop + "]");
                            return
                        }
                        chain += "[___" + prop + "]"
                    } else {
                        chain += "[" + prop + "]"
                    }
                } else {
                    chain += "." + prop
                }
                prevDot = false;
                output.push("typeof " + chain + ' !== "undefined"')
            });
            return "(" + output.join(" && ") + ")"
        }
        exports.check = check;
        exports.escapeVarName = function(variable, context, args) {
            if (variable === "") {
                return ""
            }
            if (_.isArray(variable)) {
                _.each(variable, function(val, key) {
                    variable[key] = exports.escapeVarName(val, context)
                });
                return variable
            }
            variable = variable.replace(/^this/, "_this.__currentContext");
            if (exports.isLiteral(variable)) {
                return variable
            }
            if (typeof context === "string" && context.length) {
                variable = context + "." + variable
            }
            var chain = "",
                props = variable.split(/(\.|\[|\])/),
                inArr = false,
                prevDot = false;
            props = _.reject(props, function(val) {
                return val === ""
            });
            props = filterVariablePath(props);
            _.each(props, function(prop) {
                if (prop === ".") {
                    prevDot = true;
                    return
                }
                if (prop === "[") {
                    inArr = true;
                    return
                }
                if (prop === "]") {
                    inArr = false;
                    return
                }
                if (!chain) {
                    chain = prop
                } else if (inArr) {
                    if (!exports.isStringLiteral(prop)) {
                        if (prevDot) {
                            chain = chain.replace(/\]$/, "_" + prop + "]")
                        } else {
                            chain += "[___" + prop + "]"
                        }
                    } else {
                        chain += "[" + prop + "]"
                    }
                } else {
                    chain += "." + prop
                }
                prevDot = false
            });
            return "(typeof " + chain + " === 'function') ? " + chain + "(" + args + ") : " + chain
        };
        exports.wrapArgs = function(args) {
            if (!args) {
                return {
                    declarations: "",
                    args: ""
                }
            }
            var declarations = "";
            args = _.map(args.split(","), function(value) {
                var varname, stripped = value.replace(/^\s+|\s+$/g, "");
                try {
                    varname = "__" + parser.parseVariable(stripped).name.replace(/\W/g, "_")
                } catch (e) {
                    return value
                }
                if (exports.isValidName(stripped)) {
                    declarations += exports.setVar(varname, parser.parseVariable(stripped));
                    return varname
                }
                return value
            });
            return {
                declarations: declarations,
                args: args && args.length ? args.join(",") : '""'
            }
        };
        exports.wrapMethod = function(variable, filter, context) {
            var output = "(function () {\n",
                args, wrappedArgs;
            variable = variable || '""';
            if (!filter) {
                return variable
            }
            wrappedArgs = exports.wrapArgs(filter.args, output);
            output += wrappedArgs.declarations;
            output += "return ";
            output += context ? context + '["' : "";
            output += filter.name;
            output += context ? '"]' : "";
            output += "(";
            output += wrappedArgs.args;
            output += ");\n";
            return output + "})()"
        };
        exports.wrapFilter = function(variable, filter) {
            var output = "",
                args = "";
            variable = variable || '""';
            if (!filter) {
                return variable
            }
            if (filters.hasOwnProperty(filter.name)) {
                args = filter.args ? variable + ", " + filter.args : variable;
                output += exports.wrapMethod(variable, {
                    name: filter.name,
                    args: args
                }, "_filters")
            } else {
                throw new Error('Filter "' + filter.name + '" not found')
            }
            return output
        };
        exports.wrapFilters = function(variable, filters, context, escape, args) {
            var output = exports.escapeVarName(variable, context, args);
            if (filters && filters.length > 0) {
                _.each(filters, function(filter) {
                    switch (filter.name) {
                        case "raw":
                            escape = false;
                            return;
                        case "e":
                        case "escape":
                            escape = filter.args || escape;
                            return;
                        default:
                            output = exports.wrapFilter(output, filter, "_filters");
                            break
                    }
                })
            }
            output = output || '""';
            if (escape) {
                output = "_filters.escape.call(this, " + output + ", " + escape + ")"
            }
            return output
        };
        exports.setVar = function(varName, argument, args) {
            var out = "",
                props, output, inArr, wrappedArgs;
            if (/\[/.test(argument.name)) {
                props = argument.name.split(/(\[|\])/);
                output = [];
                inArr = false;
                _.each(props, function(prop) {
                    if (prop === "") {
                        return
                    }
                    if (prop === "[") {
                        inArr = true;
                        return
                    }
                    if (prop === "]") {
                        inArr = false;
                        return
                    }
                    if (inArr && !exports.isStringLiteral(prop)) {
                        out += exports.setVar("___" + prop.replace(/\W/g, "_"), {
                            name: prop,
                            filters: [],
                            escape: true
                        })
                    }
                })
            }
            wrappedArgs = exports.wrapArgs(args);
            out += wrappedArgs.declarations;
            out += "var " + varName + ' = "";\n' + "if (" + check(argument.name, "_context") + ") {\n" + "  " + varName + " = " + exports.wrapFilters(argument.name, argument.filters, "_context", argument.escape, wrappedArgs.args) + ";\n" + "} else if (" + check(argument.name) + ") {\n" + "  " + varName + " = " + exports.wrapFilters(argument.name, argument.filters, null, argument.escape, wrappedArgs.args) + ";\n" + "}\n";
            if (argument.filters.length) {
                out += " else if (true) {\n";
                out += "  " + varName + " = " + exports.wrapFilters("", argument.filters, null, argument.escape, wrappedArgs.args) + ";\n";
                out += "}\n"
            }
            return out
        };
        exports.parseIfArgs = function(args, parser) {
            var operators = ["==", "<", ">", "!=", "<=", ">=", "===", "!==", "&&", "||", "in", "and", "or", "mod", "%"],
                errorString = "Bad if-syntax in `{% if " + args.join(" ") + " %}...",
                startParen = /^\(+/,
                endParen = /\)+$/,
                tokens = [],
                prevType, last, closing = 0;
            _.each(args, function(value, index) {
                var endsep = 0,
                    startsep = 0,
                    operand;
                if (startParen.test(value)) {
                    startsep = value.match(startParen)[0].length;
                    closing += startsep;
                    value = value.replace(startParen, "");
                    while (startsep) {
                        startsep -= 1;
                        tokens.push({
                            type: "separator",
                            value: "("
                        })
                    }
                }
                if (/^\![^=]/.test(value) || value === "not") {
                    if (value === "not") {
                        value = ""
                    } else {
                        value = value.substr(1)
                    }
                    tokens.push({
                        type: "operator",
                        value: "!"
                    })
                }
                if (endParen.test(value) && value.indexOf("(") === -1) {
                    if (!closing) {
                        throw new Error(errorString)
                    }
                    endsep = value.match(endParen)[0].length;
                    value = value.replace(endParen, "");
                    closing -= endsep
                }
                if (value === "in") {
                    last = tokens.pop();
                    prevType = "inindex"
                } else if (_.indexOf(operators, value) !== -1) {
                    if (prevType === "operator") {
                        throw new Error(errorString)
                    }
                    value = value.replace("and", "&&").replace("or", "||").replace("mod", "%");
                    tokens.push({
                        value: value
                    });
                    prevType = "operator"
                } else if (value !== "") {
                    if (prevType === "value") {
                        throw new Error(errorString)
                    }
                    operand = parser.parseVariable(value);
                    if (prevType === "inindex") {
                        tokens.push({
                            preout: last.preout + exports.setVar("__op" + index, operand),
                            value: "(((_.isArray(__op" + index + ") || typeof __op" + index + ' === "string") && _.indexOf(__op' + index + ", " + last.value + ") !== -1) || (typeof __op" + index + ' === "object" && ' + last.value + " in __op" + index + "))"
                        });
                        last = null
                    } else {
                        tokens.push({
                            preout: exports.setVar("__op" + index, operand),
                            value: "__op" + index
                        })
                    }
                    prevType = "value"
                }
                while (endsep) {
                    endsep -= 1;
                    tokens.push({
                        type: "separator",
                        value: ")"
                    })
                }
            });
            if (closing > 0) {
                throw new Error(errorString)
            }
            return tokens
        }
    }(helpers);
    ! function(exports) {
        var _months = {
            full: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            abbr: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        }, _days = {
            full: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            abbr: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
            alt: {
                "-1": "Yesterday",
                0: "Today",
                1: "Tomorrow"
            }
        };
        exports.defaultTZOffset = 0;
        exports.DateZ = function() {
            var members = {
                "default": ["getUTCDate", "getUTCDay", "getUTCFullYear", "getUTCHours", "getUTCMilliseconds", "getUTCMinutes", "getUTCMonth", "getUTCSeconds", "toISOString", "toGMTString", "toUTCString", "valueOf", "getTime"],
                z: ["getDate", "getDay", "getFullYear", "getHours", "getMilliseconds", "getMinutes", "getMonth", "getSeconds", "getYear", "toDateString", "toLocaleDateString", "toLocaleTimeString"],
                string: ["toLocaleString", "toString", "toTimeString"],
                zSet: ["setDate", "setFullYear", "setHours", "setMilliseconds", "setMinutes", "setMonth", "setSeconds", "setTime", "setYear"],
                set: ["setUTCDate", "setUTCFullYear", "setUTCHours", "setUTCMilliseconds", "setUTCMinutes", "setUTCMonth", "setUTCSeconds"],
                "static": ["UTC", "parse"]
            }, d = this,
                i;
            d.date = d.dateZ = arguments.length > 1 ? new Date(Date.UTC.apply(Date, arguments) + (new Date).getTimezoneOffset() * 6e4) : arguments.length === 1 ? new Date(new Date(arguments["0"])) : new Date;
            d.timezoneOffset = d.dateZ.getTimezoneOffset();

            function zeroPad(i) {
                return i < 10 ? "0" + i : i
            }
            function _toTZString() {
                var hours = zeroPad(Math.floor(Math.abs(d.timezoneOffset) / 60)),
                    minutes = zeroPad(Math.abs(d.timezoneOffset) - hours * 60),
                    prefix = d.timezoneOffset < 0 ? "+" : "-",
                    abbr = d.tzAbbreviation === undefined ? "" : " (" + d.tzAbbreviation + ")";
                return "GMT" + prefix + hours + minutes + abbr
            }
            _.each(members.z, function(name) {
                d[name] = function() {
                    return d.dateZ[name]()
                }
            });
            _.each(members.string, function(name) {
                d[name] = function() {
                    return d.dateZ[name].apply(d.dateZ, []).replace(/GMT[+\-]\\d{4} \\(([a-zA-Z]{3,4})\\)/, _toTZString())
                }
            });
            _.each(members["default"], function(name) {
                d[name] = function() {
                    return d.date[name]()
                }
            });
            _.each(members["static"], function(name) {
                d[name] = function() {
                    return Date[name].apply(Date, arguments)
                }
            });
            _.each(members.zSet, function(name) {
                d[name] = function() {
                    d.dateZ[name].apply(d.dateZ, arguments);
                    d.date = new Date(d.dateZ.getTime() - d.dateZ.getTimezoneOffset() * 6e4 + d.timezoneOffset * 6e4);
                    return d
                }
            });
            _.each(members.set, function(name) {
                d[name] = function() {
                    d.date[name].apply(d.date, arguments);
                    d.dateZ = new Date(d.date.getTime() + d.date.getTimezoneOffset() * 6e4 - d.timezoneOffset * 6e4);
                    return d
                }
            });
            if (exports.defaultTZOffset) {
                this.setTimezoneOffset(exports.defaultTZOffset)
            }
        };
        exports.DateZ.prototype = {
            getTimezoneOffset: function() {
                return this.timezoneOffset
            },
            setTimezoneOffset: function(offset, abbr) {
                this.timezoneOffset = offset;
                if (abbr) {
                    this.tzAbbreviation = abbr
                }
                this.dateZ = new Date(this.date.getTime() + this.date.getTimezoneOffset() * 6e4 - this.timezoneOffset * 6e4);
                return this
            }
        };
        exports.d = function(input) {
            return (input.getDate() < 10 ? "0" : "") + input.getDate()
        };
        exports.D = function(input) {
            return _days.abbr[input.getDay()]
        };
        exports.j = function(input) {
            return input.getDate()
        };
        exports.l = function(input) {
            return _days.full[input.getDay()]
        };
        exports.N = function(input) {
            var d = input.getDay();
            return d >= 1 ? d + 1 : 7
        };
        exports.S = function(input) {
            var d = input.getDate();
            return d % 10 === 1 && d !== 11 ? "st" : d % 10 === 2 && d !== 12 ? "nd" : d % 10 === 3 && d !== 13 ? "rd" : "th"
        };
        exports.w = function(input) {
            return input.getDay()
        };
        exports.z = function(input, offset, abbr) {
            var year = input.getFullYear(),
                e = new exports.DateZ(year, input.getMonth(), input.getDate(), 12, 0, 0),
                d = new exports.DateZ(year, 0, 1, 12, 0, 0);
            e.setTimezoneOffset(offset, abbr);
            d.setTimezoneOffset(offset, abbr);
            return Math.round((e - d) / 864e5)
        };
        exports.W = function(input) {
            var target = new Date(input.valueOf()),
                dayNr = (input.getDay() + 6) % 7,
                fThurs;
            target.setDate(target.getDate() - dayNr + 3);
            fThurs = target.valueOf();
            target.setMonth(0, 1);
            if (target.getDay() !== 4) {
                target.setMonth(0, 1 + (4 - target.getDay() + 7) % 7)
            }
            return 1 + Math.ceil((fThurs - target) / 6048e5)
        };
        exports.F = function(input) {
            return _months.full[input.getMonth()]
        };
        exports.m = function(input) {
            return (input.getMonth() < 9 ? "0" : "") + (input.getMonth() + 1)
        };
        exports.M = function(input) {
            return _months.abbr[input.getMonth()]
        };
        exports.n = function(input) {
            return input.getMonth() + 1
        };
        exports.t = function(input) {
            return 32 - new Date(input.getFullYear(), input.getMonth(), 32).getDate()
        };
        exports.L = function(input) {
            return new Date(input.getFullYear(), 1, 29).getDate() === 29
        };
        exports.o = function(input) {
            var target = new Date(input.valueOf());
            target.setDate(target.getDate() - (input.getDay() + 6) % 7 + 3);
            return target.getFullYear()
        };
        exports.Y = function(input) {
            return input.getFullYear()
        };
        exports.y = function(input) {
            return input.getFullYear().toString().substr(2)
        };
        exports.a = function(input) {
            return input.getHours() < 12 ? "am" : "pm"
        };
        exports.A = function(input) {
            return input.getHours() < 12 ? "AM" : "PM"
        };
        exports.B = function(input) {
            var hours = input.getUTCHours(),
                beats;
            hours = hours === 23 ? 0 : hours + 1;
            beats = Math.abs(((hours * 60 + input.getUTCMinutes()) * 60 + input.getUTCSeconds()) / 86.4).toFixed(0);
            return "000".concat(beats).slice(beats.length)
        };
        exports.g = function(input) {
            var h = input.getHours();
            return h === 0 ? 12 : h > 12 ? h - 12 : h
        };
        exports.G = function(input) {
            return input.getHours()
        };
        exports.h = function(input) {
            var h = input.getHours();
            return (h < 10 || 12 < h && 22 > h ? "0" : "") + (h < 12 ? h : h - 12)
        };
        exports.H = function(input) {
            var h = input.getHours();
            return (h < 10 ? "0" : "") + h
        };
        exports.i = function(input) {
            var m = input.getMinutes();
            return (m < 10 ? "0" : "") + m
        };
        exports.s = function(input) {
            var s = input.getSeconds();
            return (s < 10 ? "0" : "") + s
        };
        exports.O = function(input) {
            var tz = input.getTimezoneOffset();
            return (tz < 0 ? "-" : "+") + (tz / 60 < 10 ? "0" : "") + Math.abs(tz / 60) + "00"
        };
        exports.Z = function(input) {
            return input.getTimezoneOffset() * 60
        };
        exports.c = function(input) {
            return input.toISOString()
        };
        exports.r = function(input) {
            return input.toUTCString()
        };
        exports.U = function(input) {
            return input.getTime() / 1e3
        }
    }(dateformat);
    ! function(exports) {
        exports.add = function(input, addend) {
            if (_.isArray(input) && _.isArray(addend)) {
                return input.concat(addend)
            }
            if (typeof input === "object" && typeof addend === "object") {
                return _.extend(input, addend)
            }
            if (_.isNumber(input) && _.isNumber(addend)) {
                return input + addend
            }
            return input + addend
        };
        exports.addslashes = function(input) {
            if (typeof input === "object") {
                _.each(input, function(value, key) {
                    input[key] = exports.addslashes(value)
                });
                return input
            }
            return input.replace(/\\/g, "\\\\").replace(/\'/g, "\\'").replace(/\"/g, '\\"')
        };
        exports.capitalize = function(input) {
            if (typeof input === "object") {
                _.each(input, function(value, key) {
                    input[key] = exports.capitalize(value)
                });
                return input
            }
            return input.toString().charAt(0).toUpperCase() + input.toString().substr(1).toLowerCase()
        };
        exports.date = function(input, format, offset, abbr) {
            var l = format.length,
                date = new dateformat.DateZ(input),
                cur, i = 0,
                out = "";
            if (offset) {
                date.setTimezoneOffset(offset, abbr)
            }
            for (i; i < l; i += 1) {
                cur = format.charAt(i);
                if (dateformat.hasOwnProperty(cur)) {
                    out += dateformat[cur](date, offset, abbr)
                } else {
                    out += cur
                }
            }
            return out
        };
        exports["default"] = function(input, def) {
            return typeof input !== "undefined" && (input || typeof input === "number") ? input : def
        };
        exports.escape = exports.e = function(input, type) {
            type = type || "html";
            if (typeof input === "string") {
                if (type === "js") {
                    var i = 0,
                        code, out = "";
                    input = input.replace(/\\/g, "\\u005C");
                    for (i; i < input.length; i += 1) {
                        code = input.charCodeAt(i);
                        if (code < 32) {
                            code = code.toString(16).toUpperCase();
                            code = code.length < 2 ? "0" + code : code;
                            out += "\\u00" + code
                        } else {
                            out += input[i]
                        }
                    }
                    return out.replace(/&/g, "\\u0026").replace(/</g, "\\u003C").replace(/>/g, "\\u003E").replace(/\'/g, "\\u0027").replace(/"/g, "\\u0022").replace(/\=/g, "\\u003D").replace(/-/g, "\\u002D").replace(/;/g, "\\u003B")
                }
                return input.replace(/&(?!amp;|lt;|gt;|quot;|#39;)/g, "&").replace(/</g, "<").replace(/>/g, ">").replace(/"/g, "'").replace(/'/g, "'")
            }
            return input
        };
        exports.first = function(input) {
            if (typeof input === "object" && !_.isArray(input)) {
                return ""
            }
            if (typeof input === "string") {
                return input.substr(0, 1)
            }
            return _.first(input)
        };
        exports.join = function(input, separator) {
            if (_.isArray(input)) {
                return input.join(separator)
            }
            if (typeof input === "object") {
                var out = [];
                _.each(input, function(value, key) {
                    out.push(value)
                });
                return out.join(separator)
            }
            return input
        };
        exports.json_encode = function(input, indent) {
            return JSON.stringify(input, null, indent || 0)
        };
        exports.last = function(input) {
            if (typeof input === "object" && !_.isArray(input)) {
                return ""
            }
            if (typeof input === "string") {
                return input.charAt(input.length - 1)
            }
            return _.last(input)
        };
        exports.length = function(input) {
            if (typeof input === "object") {
                return _.keys(input).length
            }
            return input.length
        };
        exports.lower = function(input) {
            if (typeof input === "object") {
                _.each(input, function(value, key) {
                    input[key] = exports.lower(value)
                });
                return input
            }
            return input.toString().toLowerCase()
        };
        exports.replace = function(input, search, replacement, flags) {
            var r = new RegExp(search, flags);
            return input.replace(r, replacement)
        };
        exports.reverse = function(input) {
            if (_.isArray(input)) {
                return input.reverse()
            }
            return input
        };
        exports.striptags = function(input) {
            if (typeof input === "object") {
                _.each(input, function(value, key) {
                    input[key] = exports.striptags(value)
                });
                return input
            }
            return input.toString().replace(/(<([^>]+)>)/gi, "")
        };
        exports.title = function(input) {
            if (typeof input === "object") {
                _.each(input, function(value, key) {
                    input[key] = exports.title(value)
                });
                return input
            }
            return input.toString().replace(/\w\S*/g, function(str) {
                return str.charAt(0).toUpperCase() + str.substr(1).toLowerCase()
            })
        };
        exports.uniq = function(input) {
            return _.uniq(input)
        };
        exports.upper = function(input) {
            if (typeof input === "object") {
                _.each(input, function(value, key) {
                    input[key] = exports.upper(value)
                });
                return input
            }
            return input.toString().toUpperCase()
        };
        exports.url_encode = function(input) {
            return encodeURIComponent(input)
        };
        exports.url_decode = function(input) {
            return decodeURIComponent(input)
        }
    }(filters);
    ! function(exports) {
        var variableRegexp = /^\{\{[^\r]*?\}\}$/,
            logicRegexp = /^\{%[^\r]*?%\}$/,
            commentRegexp = /^\{#[^\r]*?#\}$/,
            TEMPLATE = exports.TEMPLATE = 0,
            LOGIC_TOKEN = 1,
            VAR_TOKEN = 2;
        exports.TOKEN_TYPES = {
            TEMPLATE: TEMPLATE,
            LOGIC: LOGIC_TOKEN,
            VAR: VAR_TOKEN
        };

        function getMethod(input) {
            return helpers.stripWhitespace(input).match(/^[\w\.]+/)[0]
        }
        function doubleEscape(input) {
            return input.replace(/\\/g, "\\\\")
        }
        function getArgs(input) {
            return doubleEscape(helpers.stripWhitespace(input).replace(/^[\w\.]+\(|\)$/g, ""))
        }
        function getContextVar(varName, context) {
            var a = varName.split(".");
            while (a.length) {
                context = context[a.splice(0, 1)[0]]
            }
            return context
        }
        function getTokenArgs(token, parts) {
            parts = _.map(parts, doubleEscape);
            var i = 0,
                l = parts.length,
                arg, ender, out = [];

            function concat(from, ending) {
                var end = new RegExp("\\" + ending + "$"),
                    i = from,
                    out = "";
                while (!end.test(out) && i < parts.length) {
                    out += " " + parts[i];
                    parts[i] = null;
                    i += 1
                }
                if (!end.test(out)) {
                    throw new Error("Malformed arguments " + out + " sent to tag.")
                }
                return out.replace(/^ /, "")
            }
            for (i; i < l; i += 1) {
                arg = parts[i];
                if (arg === null || /^\s+$/.test(arg)) {
                    continue
                }
                if (/^\"/.test(arg) && !/\"[\]\}]?$/.test(arg) || /^\'/.test(arg) && !/\'[\]\}]?$/.test(arg) || /^\{/.test(arg) && !/\}$/.test(arg) || /^\[/.test(arg) && !/\]$/.test(arg)) {
                    switch (arg.substr(0, 1)) {
                        case "'":
                            ender = "'";
                            break;
                        case '"':
                            ender = '"';
                            break;
                        case "[":
                            ender = "]";
                            break;
                        case "{":
                            ender = "}";
                            break
                    }
                    out.push(concat(i, ender));
                    continue
                }
                out.push(arg)
            }
            return out
        }
        function findSubBlocks(topToken, blocks) {
            _.each(topToken.tokens, function(token, index) {
                if (token.name === "block") {
                    blocks[token.args[0]] = token;
                    findSubBlocks(token, blocks)
                }
            })
        }
        function getParentBlock(token) {
            var block;
            if (token.parentBlock) {
                block = token.parentBlock
            } else if (token.parent) {
                block = getParentBlock(_.last(token.parent))
            }
            return block
        }
        exports.parseVariable = function(token, escape) {
            if (!token) {
                return {
                    type: null,
                    name: "",
                    filters: [],
                    escape: escape
                }
            }
            var filters = [],
                parts = token.replace(/^\{\{\s*|\s*\}\}$/g, "").split("|"),
                varname = parts.shift(),
                args = null,
                part;
            if (/\(/.test(varname)) {
                args = getArgs(varname.replace(/^\w+\./, ""));
                varname = getMethod(varname)
            }
            _.each(parts, function(part, i) {
                if (part && (/^[\w\.]+\(/.test(part) || /\)$/.test(part)) && !/^[\w\.]+\([^\)]*\)$/.test(part)) {
                    parts[i] += parts[i + 1] ? "|" + parts[i + 1] : "";
                    parts[i + 1] = false
                }
            });
            parts = _.without(parts, false);
            _.each(parts, function(part) {
                var filter_name = getMethod(part);
                if (/\(/.test(part)) {
                    filters.push({
                        name: filter_name,
                        args: getArgs(part)
                    })
                } else {
                    filters.push({
                        name: filter_name,
                        args: ""
                    })
                }
            });
            return {
                type: VAR_TOKEN,
                name: varname,
                args: args,
                filters: filters,
                escape: escape
            }
        };
        exports.parse = function(data, tags, autoescape) {
            var rawtokens = helpers.stripWhitespace(data).split(/(\{%[^\r]*?%\}|\{\{.*?\}\}|\{#[^\r]*?#\})/),
                escape = !! autoescape,
                last_escape = escape,
                stack = [
                    []
                ],
                index = 0,
                i = 0,
                j = rawtokens.length,
                token, parts, tagname, lines = 1,
                curline = 1,
                newlines = null,
                lastToken, rawStart = /^\{\% *raw *\%\}/,
                rawEnd = /\{\% *endraw *\%\}$/,
                inRaw = false,
                stripAfter = false,
                stripBefore = false,
                stripStart = false,
                stripEnd = false;
            for (i; i < j; i += 1) {
                token = rawtokens[i];
                curline = lines;
                newlines = token.match(/\n/g);
                stripAfter = false;
                stripBefore = false;
                stripStart = false;
                stripEnd = false;
                if (newlines) {
                    lines += newlines.length
                }
                if (inRaw !== false && !rawEnd.test(token)) {
                    inRaw += token;
                    continue
                }
                if (token.length === 0 || commentRegexp.test(token)) {
                    continue
                } else if (/^\s+$/.test(token)) {
                    token = token.replace(/ +/, " ").replace(/\n+/, "\n")
                } else if (variableRegexp.test(token)) {
                    token = exports.parseVariable(token, escape)
                } else if (logicRegexp.test(token)) {
                    if (rawEnd.test(token)) {
                        token = inRaw + token.replace(rawEnd, "");
                        inRaw = false;
                        stack[index].push(token);
                        continue
                    }
                    if (rawStart.test(token)) {
                        inRaw = token.replace(rawStart, "");
                        continue
                    }
                    parts = token.replace(/^\{%\s*|\s*%\}$/g, "").split(" ");
                    if (parts[0] === "-") {
                        stripBefore = true;
                        parts.shift()
                    }
                    tagname = parts.shift();
                    if (_.last(parts) === "-") {
                        stripAfter = true;
                        parts.pop()
                    }
                    if (index > 0 && /^end/.test(tagname)) {
                        lastToken = _.last(stack[stack.length - 2]);
                        if ("end" + lastToken.name === tagname) {
                            if (lastToken.name === "autoescape") {
                                escape = last_escape
                            }
                            lastToken.strip.end = stripBefore;
                            lastToken.strip.after = stripAfter;
                            stack.pop();
                            index -= 1;
                            continue
                        }
                        throw new Error('Expected end tag for "' + lastToken.name + '", but found "' + tagname + '" at line ' + lines + ".")
                    }
                    if (!tags.hasOwnProperty(tagname)) {
                        throw new Error("Unknown logic tag at line " + lines + ': "' + tagname + '".')
                    }
                    if (tagname === "autoescape") {
                        last_escape = escape;
                        escape = !parts.length || parts[0] === "true" ? parts.length >= 2 ? parts[1] : true : false
                    }
                    token = {
                        type: LOGIC_TOKEN,
                        line: curline,
                        name: tagname,
                        compile: tags[tagname],
                        parent: _.uniq(stack[stack.length - 2] || []),
                        strip: {
                            before: stripBefore,
                            after: stripAfter,
                            start: false,
                            end: false
                        }
                    };
                    token.args = getTokenArgs(token, parts);
                    if (tags[tagname].ends) {
                        token.strip.after = false;
                        token.strip.start = stripAfter;
                        stack[index].push(token);
                        stack.push(token.tokens = []);
                        index += 1;
                        continue
                    }
                }
                stack[index].push(token)
            }
            if (inRaw !== false) {
                throw new Error('Missing expected end tag for "raw" on line ' + curline + ".")
            }
            if (index !== 0) {
                lastToken = _.last(stack[stack.length - 2]);
                throw new Error('Missing end tag for "' + lastToken.name + '" that was opened on line ' + lastToken.line + ".")
            }
            return stack[index]
        };

        function precompile(indent, context) {
            var filepath, extendsHasVar, preservedTokens = [];
            if (this.type === TEMPLATE) {
                _.each(this.tokens, function(token, index) {
                    if (!extendsHasVar) {
                        if (token.name === "extends") {
                            filepath = token.args[0];
                            if (!helpers.isStringLiteral(filepath)) {
                                if (!context) {
                                    extendsHasVar = true;
                                    return
                                }
                                filepath = '"' + getContextVar(filepath, context) + '"'
                            }
                            if (!helpers.isStringLiteral(filepath) || token.args.length > 1) {
                                throw new Error("Extends tag on line " + token.line + " accepts exactly one string literal as an argument.")
                            }
                            if (index > 0) {
                                throw new Error('Extends tag must be the first tag in the template, but "extends" found on line ' + token.line + ".")
                            }
                            token.template = this.compileFile(filepath.replace(/['"]/g, ""), true);
                            this.parent = token.template;
                            this.blocks = _.extend({}, this.parent.blocks, this.blocks)
                        } else if (token.name === "block") {
                            var blockname = token.args[0],
                                parentBlockIndex;
                            if (!helpers.isValidBlockName(blockname) || token.args.length !== 1) {
                                throw new Error('Invalid block tag name "' + blockname + '" on line ' + token.line + ".")
                            }
                            this.blocks[blockname] = token;
                            findSubBlocks(token, this.blocks);
                            if (this.parent) {
                                token.parentBlock = this.parent.blocks[blockname];
                                parentBlockIndex = _.indexOf(this.parent.tokens, this.parent.blocks[blockname]);
                                if (parentBlockIndex >= 0) {
                                    this.parent.tokens[parentBlockIndex] = token
                                }
                            }
                        } else if (token.type === LOGIC_TOKEN) {
                            preservedTokens.push(token)
                        }
                    }
                }, this);
                if (extendsHasVar) {
                    return false
                }
                if (this.parent && this.parent.tokens) {
                    this.tokens = preservedTokens.concat(this.parent.tokens)
                }
            }
        }
        exports.compile = function compile(indent, context, template) {
            var code = "",
                wrappedInMethod, blockname, parentBlock;
            indent = indent || "";
            if (this.type === TEMPLATE) {
                template = this
            }
            if (!this.blocks) {
                this.blocks = {}
            }
            if (precompile.call(this, indent, context) === false) {
                return false
            }
            _.each(this.tokens, function(token, index) {
                var name, key, args, prev, next;
                if (typeof token === "string") {
                    prev = this.tokens[index - 1];
                    next = this.tokens[index + 1];
                    if (prev && prev.strip && prev.strip.after) {
                        token = token.replace(/^\s+/, "")
                    }
                    if (next && next.strip && next.strip.before) {
                        token = token.replace(/\s+$/, "")
                    }
                    code += '_output += "' + doubleEscape(token).replace(/\n/g, "\\n").replace(/\r/g, "\\r").replace(/"/g, '\\"') + '";\n';
                    return code
                }
                if (typeof token !== "object") {
                    return
                }
                if (token.type === VAR_TOKEN) {
                    name = token.name.replace(/\W/g, "_");
                    key = helpers.isLiteral(name) ? '["' + name + '"]' : "." + name;
                    args = token.args && token.args.length ? token.args : "";
                    code += 'if (typeof _context !== "undefined" && typeof _context' + key + ' === "function") {\n';
                    wrappedInMethod = helpers.wrapMethod("", {
                        name: name,
                        args: args
                    }, "_context");
                    code += '  _output = (typeof _output === "undefined") ? ' + wrappedInMethod + ": _output + " + wrappedInMethod + ";\n";
                    if (helpers.isValidName(name)) {
                        code += "} else if (typeof " + name + ' === "function") {\n';
                        wrappedInMethod = helpers.wrapMethod("", {
                            name: name,
                            args: args
                        });
                        code += '  _output = (typeof _output === "undefined") ? ' + wrappedInMethod + ": _output + " + wrappedInMethod + ";\n"
                    }
                    code += "} else {\n";
                    code += helpers.setVar("__" + name, token, args);
                    code += '  _output = (typeof _output === "undefined") ? __' + name + ": _output + __" + name + ";\n";
                    code += "}\n"
                }
                if (token.type !== LOGIC_TOKEN) {
                    return
                }
                if (token.name === "block") {
                    blockname = token.args[0];
                    if (!template.blocks.hasOwnProperty(blockname)) {
                        throw new Error('Unrecognized nested block.  Block "' + blockname + '" at line ' + token.line + ' of "' + template.id + '" is not in template block list.')
                    }
                    code += compile.call(template.blocks[token.args[0]], indent + "  ", context, template)
                } else if (token.name === "parent") {
                    parentBlock = getParentBlock(token);
                    if (!parentBlock) {
                        throw new Error("No parent block found for parent tag at line " + token.line + ".")
                    }
                    code += compile.call(parentBlock, indent + "  ", context)
                } else if (token.hasOwnProperty("compile")) {
                    if (token.strip.start && token.tokens.length && typeof token.tokens[0] === "string") {
                        token.tokens[0] = token.tokens[0].replace(/^\s+/, "")
                    }
                    if (token.strip.end && token.tokens.length && typeof _.last(token.tokens) === "string") {
                        token.tokens[token.tokens.length - 1] = _.last(token.tokens).replace(/\s+$/, "")
                    }
                    code += token.compile(indent + "  ", exports)
                } else {
                    code += compile.call(token, indent + "  ", context)
                }
            }, this);
            return code
        }
    }(parser);
    tags["autoescape"] = function() {
        module = {};
        module.exports = function(indent, parser) {
            return parser.compile.apply(this, [indent])
        };
        module.exports.ends = true;
        return module.exports
    }();
    tags["block"] = function() {
        module = {};
        module.exports = {
            ends: true
        };
        return module.exports
    }();
    tags["else"] = function() {
        module = {};
        module.exports = function(indent, parser) {
            var last = _.last(this.parent).name,
                thisArgs = _.clone(this.args),
                ifarg, args, out;
            if (last === "for") {
                if (thisArgs.length) {
                    throw new Error('"else" tag cannot accept arguments in the "for" context.')
                }
                return "} if (__loopLength === 0) {\n"
            }
            if (last !== "if") {
                throw new Error('Cannot call else tag outside of "if" or "for" context.')
            }
            ifarg = thisArgs.shift();
            args = helpers.parseIfArgs(thisArgs, parser);
            out = "";
            if (ifarg) {
                out += "} else if (\n";
                out += "  (function () {\n";
                _.each(args, function(token) {
                    if (token.hasOwnProperty("preout") && token.preout) {
                        out += token.preout + "\n"
                    }
                });
                out += "return (\n";
                _.each(args, function(token) {
                    out += token.value + " "
                });
                out += ");\n";
                out += "  })()\n";
                out += ") {\n";
                return out
            }
            return indent + "\n} else {\n"
        };
        return module.exports
    }();
    tags["extends"] = function() {
        module = {};
        module.exports = {};
        return module.exports
    }();
    tags["filter"] = function() {
        module = {};
        module.exports = function(indent, parser) {
            var thisArgs = _.clone(this.args),
                name = thisArgs.shift(),
                args = thisArgs.length ? thisArgs.join(", ") : "",
                value = "(function () {\n";
            value += '  var _output = "";\n';
            value += parser.compile.apply(this, [indent + "  "]) + "\n";
            value += "  return _output;\n";
            value += "})()\n";
            return "_output += " + helpers.wrapFilter(value.replace(/\n/g, ""), {
                name: name,
                args: args
            }) + ";\n"
        };
        module.exports.ends = true;
        return module.exports
    }();
    tags["for"] = function() {
        module = {};
        module.exports = function(indent, parser) {
            var thisArgs = _.clone(this.args),
                operand1 = thisArgs[0],
                operator = thisArgs[1],
                operand2 = parser.parseVariable(thisArgs[2]),
                out = "",
                loopShared;
            indent = indent || "";
            if (typeof operator !== "undefined" && operator !== "in") {
                throw new Error('Invalid syntax in "for" tag')
            }
            if (!helpers.isValidShortName(operand1)) {
                throw new Error("Invalid arguments (" + operand1 + ') passed to "for" tag')
            }
            loopShared = "loop.index = __loopIndex + 1;\n" + "loop.index0 = __loopIndex;\n" + "loop.revindex = __loopLength - loop.index0;\n" + "loop.revindex0 = loop.revindex - 1;\n" + "loop.first = (__loopIndex === 0);\n" + "loop.last = (__loopIndex === __loopLength - 1);\n" + '_context["' + operand1 + '"] = __loopIter[loop.key];\n' + parser.compile.apply(this, [indent + "   "]);
            out = "(function () {\n" + "  var loop = {}, __loopKey, __loopIndex = 0, __loopLength = 0, __keys = []," + '    __ctx_operand = _context["' + operand1 + '"],\n' + "    loop_cycle = function() {\n" + "      var args = _.toArray(arguments), i = loop.index0 % args.length;\n" + "      return args[i];\n" + "    };\n" + helpers.setVar("__loopIter", operand2) + "  else {\n" + "    return;\n" + "  }\n" + "  if (_.isArray(__loopIter)) {\n" + "    __loopIndex = 0; __loopLength = __loopIter.length;\n" + "    for (; __loopIndex < __loopLength; __loopIndex += 1) {\n" + "       loop.key = __loopIndex;\n" + loopShared + "    }\n" + '  } else if (typeof __loopIter === "object") {\n' + "    __keys = _.keys(__loopIter);\n" + "    __loopLength = __keys.length;\n" + "    __loopIndex = 0;\n" + "    for (; __loopIndex < __loopLength; __loopIndex += 1) {\n" + "       loop.key = __keys[__loopIndex];\n" + loopShared + "    }\n" + "  }\n" + '  _context["' + operand1 + '"] = __ctx_operand;\n' + "})();\n";
            return out
        };
        module.exports.ends = true;
        return module.exports
    }();
    tags["if"] = function() {
        module = {};
        module.exports = function(indent, parser) {
            var thisArgs = _.clone(this.args),
                args = helpers.parseIfArgs(thisArgs, parser),
                out = "(function () {\n";
            _.each(args, function(token) {
                if (token.hasOwnProperty("preout") && token.preout) {
                    out += token.preout + "\n"
                }
            });
            out += "\nif (\n";
            _.each(args, function(token) {
                out += token.value + " "
            });
            out += ") {\n";
            out += parser.compile.apply(this, [indent + "  "]);
            out += "\n}\n";
            out += "})();\n";
            return out
        };
        module.exports.ends = true;
        return module.exports
    }();
    tags["import"] = function() {
        module = {};
        module.exports = function(indent, parser) {
            if (this.args.length !== 3) {}
            var thisArgs = _.clone(this.args),
                file = thisArgs[0],
                as = thisArgs[1],
                name = thisArgs[2],
                out = "";
            if (!helpers.isLiteral(file) && !helpers.isValidName(file)) {
                throw new Error('Invalid attempt to import "' + file + '".')
            }
            if (as !== "as") {
                throw new Error('Invalid syntax {% import "' + file + '" ' + as + " " + name + " %}")
            }
            out += "_.extend(_context, (function () {\n";
            out += 'var _context = {}, __ctx = {}, _output = "";\n' + helpers.setVar("__template", parser.parseVariable(file)) + "_this.compileFile(__template).render(__ctx, _parents);\n" + "_.each(__ctx, function (item, key) {\n" + '  if (typeof item === "function") {\n' + '    _context["' + name + '_" + key] = item;\n' + "  }\n" + "});\n" + "return _context;\n";
            out += "})());\n";
            return out
        };
        return module.exports
    }();
    tags["include"] = function() {
        module = {};
        module.exports = function(indent, parser) {
            var args = _.clone(this.args),
                template = args.shift(),
                context = "_context",
                ignore = false,
                out = "",
                ctx;
            indent = indent || "";
            if (!helpers.isLiteral(template) && !helpers.isValidName(template)) {
                throw new Error("Invalid arguments passed to 'include' tag.")
            }
            if (args.length) {
                if (_.last(args) === "only") {
                    context = "{}";
                    args.pop()
                }
                if (args.length > 1 && args[0] === "ignore" & args[1] === "missing") {
                    args.shift();
                    args.shift();
                    ignore = true
                }
                if (args.length && args[0] !== "with") {
                    throw new Error("Invalid arguments passed to 'include' tag.")
                }
                if (args[0] === "with") {
                    args.shift();
                    if (!args.length) {
                        throw new Error("Context for 'include' tag not provided, but expected after 'with' token.")
                    }
                    ctx = args.shift();
                    context = '_context["' + ctx + '"] || ' + ctx
                }
            }
            out = "(function () {\n" + helpers.setVar("__template", parser.parseVariable(template)) + "\n" + "  var includeContext = " + context + ";\n";
            if (ignore) {
                out += "try {\n"
            }
            out += '  if (typeof __template === "string") {\n';
            out += "    _output += _this.compileFile(__template).render(includeContext, _parents);\n";
            out += "  }\n";
            if (ignore) {
                out += "} catch (e) {}\n"
            }
            out += "})();\n";
            return out
        };
        return module.exports
    }();
    tags["macro"] = function() {
        module = {};
        module.exports = function(indent, parser) {
            var thisArgs = _.clone(this.args),
                macro = thisArgs.shift(),
                args = "",
                out = "";
            if (thisArgs.length) {
                args = JSON.stringify(thisArgs).replace(/^\[|\'|\"|\]$/g, "")
            }
            out += "_context." + macro + " = function (" + args + ") {\n";
            out += '  var _output = "";\n';
            out += parser.compile.apply(this, [indent + "  "]);
            out += "  return _output;\n";
            out += "};\n";
            return out
        };
        module.exports.ends = true;
        return module.exports
    }();
    tags["parent"] = function() {
        module = {};
        module.exports = {};
        return module.exports
    }();
    tags["raw"] = function() {
        module = {};
        module.exports = {
            ends: true
        };
        return module.exports
    }();
    tags["set"] = function() {
        module = {};
        module.exports = function(indent, parser) {
            var thisArgs = _.clone(this.args),
                varname = helpers.escapeVarName(thisArgs.shift(), "_context"),
                value;
            if (thisArgs.shift() !== "=") {
                throw new Error('Invalid token "' + thisArgs[1] + '" in {% set ' + thisArgs[0] + ' %}. Missing "=".')
            }
            value = thisArgs[0];
            if (helpers.isLiteral(value) || /^\{|^\[/.test(value) || value === "true" || value === "false") {
                return " " + varname + " = " + value + ";"
            }
            value = parser.parseVariable(value);
            return " " + varname + " = " + "(function () {\n" + "  var _output;\n" + parser.compile.apply({
                tokens: [value]
            }, [indent]) + "\n" + "  return _output;\n" + "})();\n"
        };
        return module.exports
    }();
    tags["spaceless"] = function() {
        module = {};
        module.exports = function(indent, parser) {
            var output = [],
                i = this.tokens.length - 1;
            for (i; i >= 0; i -= 1) {
                this.tokens[i] = this.tokens[i].replace(/^\s+/gi, "").replace(/>\s+</gi, "><").replace(/\s+$/gi, "")
            }
            output.push(parser.compile.call(this, indent + "    "));
            return output.join("")
        };
        module.exports.ends = true;
        return module.exports
    }();
    return swig
}();