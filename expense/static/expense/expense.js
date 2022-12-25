document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener("click", (event) => {
        const element = event.target
        
        // console.log(element)

        if (element.id === "update-category") {
            selected_category_id = element.parentElement.dataset['category_id']
            fillUpdateCategory(selected_category_id)
        }
        else if (element.id === "save-category") {
            selected_category_id = element.dataset['category_id']
            updateCategory(selected_category_id)
        }
        else if (element.id === "delete-category") {
            selected_category_id = element.dataset['category_id']
            deleteCategory(selected_category_id)
        }


    })
})

//preoccupy the update category form with most up-to-date data
const fillUpdateCategory = (category_id) => {
    fetch(`/update_category/${category_id}`)
    .then(response => response.json())
    .then(category => {
        category_names = [...document.querySelectorAll('#update-category-name')]
        category_initials = [...document.querySelectorAll('#update-category-initial')]
        category_colors = [...document.querySelectorAll('#update-category-color')]

        selected_category_name = category_names.find(name => name.dataset['category_id'] === selected_category_id)
        selected_category_initial = category_initials.find(initial => initial.dataset['category_id'] === selected_category_id)
        selected_category_color = category_colors.find(color => color.dataset['category_id'] === selected_category_id)

        selected_category_name.value = category.name
        selected_category_initial.value = category.initial
        selected_category_color.value = category.color
    })
}

const updateCategory = (category_id) => {
    category_names = [...document.querySelectorAll('#update-category-name')]
    category_initials = [...document.querySelectorAll('#update-category-initial')]
    category_colors = [...document.querySelectorAll('#update-category-color')]

    selected_category_name = category_names.find(name => name.dataset['category_id'] === selected_category_id)
    selected_category_initial = category_initials.find(initial => initial.dataset['category_id'] === selected_category_id)
    selected_category_color = category_colors.find(color => color.dataset['category_id'] === selected_category_id)

    fetch(`/update_category/${category_id}`, {
        method: "put",
        body: JSON.stringify({
            name: selected_category_name.value,
            initial: selected_category_initial.value,
            color: selected_category_color.value
        })
    })
    .then(() => {
        location.reload()
    })
}

const deleteCategory = (category_id) => {
    console.log(category_id)   

    fetch(`/update_category/${category_id}`, {
        method: "put",
        body: JSON.stringify({
            delete: true
        })
    })
    .then(() => {
        location.reload()
    })
}