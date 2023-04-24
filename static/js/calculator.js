/*
 * Mini calculator code
 */
// div块元素
var result;
window.onload = function(){
	result  = document.getElementById("result");
	result.innerHTML = "";
}

// 是否进行了运算
var equal = false;

// 如果进行了运算，下次输入数前进行清零
function isEqual(){
	if (equal){
		c();
		equal = false;
	}
}

// 数字
function pn(n){
	isEqual();
	result.innerHTML += n;
}

// 符号
function po(o){
	result.innerHTML += o;
	equal = false;
}

// 左括号
function leftBracket(){
	isEqual();
	var r = result.innerHTML;
	var c = r.charAt(r.length - 1);
	if ("0" <= c && c <= "9" || c === "%"){
		po("×");
	}
	result.innerHTML += "(";
}

// 右括号
function rightBracket(){
	isEqual();
	result.innerHTML += ")"
}

// 乘方
function ppow(){
	isEqual();
	result.innerHTML += "^"
}

// 开方
function psqrt(){
	isEqual();
	var r = result.innerHTML;
	var c = r.charAt(r.length - 1);
	if ("0" <= c && c <= "9" || c === "%"){
		po("×");
	}
	result.innerHTML += "√";
}

// 清空result栏
function c(){
	result.innerHTML = "";
}

// 退格
function backspace(){
	var r = result.innerHTML;
	result.innerHTML = r.substr(0,r.length - 1);
	isEqual();
}

// 计算结果，先算乘方，再算开方，最后直接用eval求值
function equals1(){
	equal = true;
	var r = result.innerHTML;
	//将特殊字符进行替换
	r = r.replace(/×/g,"*");
	r = r.replace(/÷/g,"/");
	r = r.replace(/%/g,"*0.01");
	try{
        r = pow(r);
	    r = sqrt(r);
		result.innerHTML=eval(r);
	}catch(e){
		result.innerHTML="Input incorrect";
	}
}

// 乘方计算，注意有可能嵌套
function pow(r){
	var arr = r.split("^");
	if (arr.length === 1){
		return r;
	}
	var leftstr = leftOperation(arr[0]);
	var rightstr = rightOperation(arr[1]);
	var num =  "Math.pow(" + leftstr + "," + rightstr + ")";
	var leftr = arr[0].substring(0,arr[0].length - leftstr.length);
	var rightr = arr[1].substring(rightstr.length,arr[1].length);
	var r2 = leftr + num + rightr;
	return pow(r2);
}

// 开方计算，注意有可能嵌套
function sqrt(r){
	if (r.indexOf("√") === -1){
		return r;
	}
	var arr = r.split("√");
	var rightstr = rightOperation(arr[1]);
	var num = "Math.sqrt(" + rightstr + ")";
	var leftr = arr[0];
	var rightr = arr[1].substring(rightstr.length,arr[1].length);
	var r2 =leftr + num + rightr;
	return sqrt(r2);
}

// 找到乘方控制的左边部分
function leftOperation(r){
	var leftBracket = 0;
	var rightBracket = 0;
	var i;
	for (i = r.length - 1; i >=0; i--){
		var c = r.charAt(i);
		if (c === ")"){
			rightBracket++;
		} else if (leftBracket === rightBracket && c >="0" && c <= "9"){
			break;
		} else if (c === "("){
			leftBracket++;
		}
	}
	return r.substring(i);
}

// 找到乘方或开方控制的右半部分
function rightOperation(r){
	var leftBracket = 0;
	var rightBracket = 0;
	var i;
	for (i = 0; i <  r.length; i++){
		var c = r.charAt(i);
		if (c === "("){
			leftBracket++;
		} else if (leftBracket === rightBracket && c >="0" && c <= "9"){
			break;
		} else if (c === ")"){
			rightBracket++;
		}
	}
	return r.substring(0,i+1);
}