document.addEventListener("click", (event) => {
    const element = event.target

    // console.log(element)

    if (element.id === "uploaded-file") {
        selected_file_id = parseInt(element.dataset['file_id'])
        select_file(selected_file_id)
    }
})

document.addEventListener("DOMContentLoaded", () => {
    load_files()
})



const load_files = () => {
    fetch('/get_files')
    .then(response => response.json())
    .then(files => {
        files.forEach(displayFile)
    })
}

const displayFile = (file) => {
    newFile = document.createElement('div')
    newFile.id = 'uploaded-file'
    newFile.innerHTML = file.file_name
    newFile.dataset['file_id'] = file.file_id
    newFile.style.backgroundColor = file.selected ? "lightgrey" : "white"

    document.querySelector('#uploaded-files').append(newFile)
}

const select_file = (file_id) => {

    fetch(`/file/${file_id}`, {
        method: 'Put'
    })
    .then(response => response.json())
    .then(file => {
        targetElement = [...document.querySelectorAll('#uploaded-file')].find(file => parseInt(file.dataset['file_id']) === file_id)
        targetElement.style.backgroundColor = file.selected ? "lightgrey": "white"
    })
}