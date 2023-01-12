document.addEventListener("click", (event) => {
    const element = event.target

    // console.log(element)

    if (element.id === "uploaded-file") {
        selected_file_id = parseInt(element.dataset['file_id'])
        select_file(selected_file_id)
    }
    else if (element.id === "show-file-content") {
        load_file_contents()
    }
    else if (element.id === "delete-file") { 
        delete_selected_files()
    }
})

document.addEventListener("DOMContentLoaded", () => {
    if (window.history.replaceState) {
        window.history.replaceState(null, null, window.location.href)
    }
    load_files()
})




const load_files = () => {
    fetch('/get_files')
    .then(response => response.json())
    .then(files => {
        displayFileButtons(files.length)
        files.forEach(displayFile)
    })
}

const displayFileButtons = (file_count) => {
    const buttonContainer = document.querySelector('#file-buttons')
        if (file_count === 0) {
            buttonContainer.hidden = true
        }
        else {
            buttonContainer.hidden = false
        }
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

const delete_selected_files = () => {
    console.log("deleting selected files")
    selected_files = []

    fetch("/get_files")
    .then(response => response.json())
    .then(files => {
        files.forEach(file => {
            if (file.selected) {
                selected_files.push(file.file_id)
            }
        })

        fetch("/delete_selected_files", {
            method: "Put",
            body: JSON.stringify({
                selected_files: selected_files
            })
        })
    })
    .then(() => {
        location.reload()
    })
}

const load_file_contents = () => {
    document.querySelector('#file-expense-container').innerHTML=""

    fetch("/load_file_contents")
    .then(response => response.json())
    .then(data => {
        data.forEach((entry) => {
            newEntry = document.createElement('div')
            newEntry.innerHTML = `${entry.id}. ${entry.date}${entry.category} - ${entry.name}: $${parseFloat(entry.price).toFixed(2)}`

            document.querySelector('#file-expense-container').append(newEntry)
        })
    })
}
