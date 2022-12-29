/*
 * Random Selector Code
 * Copyright: PetroChina
 */

const tagsEl = document.getElementById('tags')
const textarea = document.getElementById('textarea')

textarea.focus()

// 监听你输入的键盘按键
textarea.addEventListener('keyup', (e)=>{
    createTags(e.target.value)

    // 如果按的是回车，等待10ms然后调用随机选择方法
    if(e.key == 'Enter') {
        setTimeout(() => {
            e.target.value = ''
        },10)

        randomSelect()
    }
})

function createTags(input){
    // 字符分割,逗号分隔，以及空格不生成一个单独的字符
    const tags = input.split('，').filter(tag => tag.trim() !== '').map(tag => tag.trim())

    tagsEl.innerHTML = ''

    // 将写入的choice加上tag，并且给它上树
    tags.forEach(tag => {
        const tagEl = document.createElement('span')
        tagEl.classList.add('tag')
        tagEl.innerText = tag
        tagsEl.appendChild(tagEl)
    })
}

function randomSelect() {
    // 进行30次随机
    const times = 30

    const interval = setInterval(()=>{
        // 拿到一个随机标签
        const randomTag = pickRandomTag()

        // 突出显示随机标签
        highlightTag(randomTag)

        // 过100ms去除随机标签，这就达到了一个在不同标签之间切换高亮的效果
        setTimeout(()=>{
            unHighlightTag(randomTag)
        },100)
    },100);

    // 3s后清除定时器
    setTimeout(()=>{
        // 清除interval定时器
        clearInterval(interval)

        // 对最终的选中的choice高亮
        setTimeout(()=>{
            const randomTag = pickRandomTag()

            highlightTag(randomTag)
        },100)

    },times * 100)
}

// 拿到一个随机标签方法
function pickRandomTag() {
    const tags = document.querySelectorAll('.tag')
    //  Math.floor()为向下取整, Math.ceil()这个是向上取整
    return tags[Math.floor(Math.random() * tags.length)]
}

// 设置被选中之后的高亮效果
function highlightTag(tag) {
    tag.classList.add('highlight')
}

function unHighlightTag(tag) {
    tag.classList.remove('highlight')
}