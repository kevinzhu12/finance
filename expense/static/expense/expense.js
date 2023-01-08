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
    else if (element.id === "delete-expense") {
        selected_category_id = element.parentElement.dataset['expense_id']
        deleteExpense(element, selected_category_id)
    }
    else if (element.id === "edit-expense") {
        selected_expense_id = element.parentElement.dataset['expense_id']
        editExpense(selected_expense_id)
    }
    else if (element.id === "edit-expense-submit") {
        selected_expense_id = (element.parentElement.parentElement.dataset['expense_id'])

        // eform = (document.getElementsByClassName('edit-expense-form')[0])
        editForm = [...document.querySelectorAll('#edit-expense-form')].find(form => form.parentElement.dataset['expense_id'] === selected_expense_id)

        update_edit_form(selected_expense_id, editForm)
    }

})

document.addEventListener("DOMContentLoaded", () => {
    load_chart()
    load_expenses()
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

const getCategories = async () => {
    var categoryList = []

    await fetch('/get_categories')
    .then(response => response.json())
    .then(category => {
        categoryList = category.categories
    })

    return categoryList
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

const get_expense = async () => {
    return fetch('/get_expenses')
    .then(response => response.json())
}

const load_expenses = async () => {
    get_expense()
    .then(data => {
        data.expenses.forEach(add_expense)
    })
}

const add_expense = (e) => {
    const expense = document.createElement('div')
    expense.id = 'expense'
    expense.dataset.expense_id = e.id
    expense.style.backgroundColor = e.category.color
    expense.innerHTML = formatExpense(e)
    document.querySelector('#expenses').append(expense)
}

const formatExpense = (e) => {
    return `
    <div id="expense-info">
        ${e.date}${e.category.initial} - ${e.item.name}: \$${e.item.price}
    </div>
    ` + expenseButtons()
}

const expenseButtons = () => {
    return `
    <button id="delete-expense">Delete</button>
    <button id="edit-expense">Edit</button>
    `
}

const deleteCategory = (category_id) => {
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

const deleteExpense = (element, expense_id) => {
    element.parentElement.style.animationPlayState = 'running'
    element.style.animationPlayState = 'running'

    editbutton = [...document.querySelectorAll("#edit-expense")].find( (edit) => {
        return edit.parentElement.dataset['expense_id'] === expense_id
    })
    editbutton.style.animationPlayState = 'running'

    expenseInfo = [...document.querySelectorAll("#expense-info")].find( (edit) => {
        return edit.parentElement.dataset['expense_id'] === expense_id
    })
    expenseInfo.style.animationPlayState = 'running'

    element.parentElement.addEventListener('animationend', () => {
        element.parentElement.remove()
    })

    //remove from DB

    fetch(`/delete_expense/${expense_id}`)
    .then(() => {
        reload_chart()
    })
}


const load_chart = async () => {
    const totalExpense = await getTotalExpense()
    
    const ctx = document.querySelector("#myChart")

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: get_expense_labels(totalExpense),
            datasets: [{
                label: 'Amount of $',
                data: get_expense_spendings(totalExpense),
                hoverOffset: 20,
                backgroundColor: get_expense_colors(totalExpense)
            }]
        },
        options: {
            radius: "95%",
        }
    })
}

const reload_chart = () => {
    var oldCanv = document.getElementById('myChart')
        var canvasContainer = oldCanv.parentElement

        canvasContainer.removeChild(oldCanv)

        var newCanv = document.createElement('canvas')
        newCanv.id = 'myChart'

        canvasContainer.appendChild(newCanv)
        load_chart()
}

const get_expense_labels = (totalExpense) => {
    let labels = []

    Object.entries(totalExpense).forEach( ([, expenseCategory]) => {
        labels.push(expenseCategory.name)
    })

    return labels
}

const get_expense_spendings = (totalExpense) => {
    let spendings = []
    Object.entries(totalExpense).forEach( ([, expenseCategory]) => {
        spendings.push(expenseCategory.totalAmount)
    })

    return spendings
}

const get_expense_colors = (totalExpense) => {
    let colors = []
    Object.entries(totalExpense).forEach( ([,expenseCategory]) => {
        colors.push(`${expenseCategory.color}`)
    })

    return colors
}

const getTotalExpense = async () => {
    var expense_data = {}

    await get_expense()
    .then(data => {
        data.expenses.forEach((expense) => {
            // console.log(expense)
            if (!(expense.category.initial in expense_data)) {
                // console.log(expense.category.initial)
                expense_data[expense.category.initial] = {
                    "name": expense.category.name,
                    "totalAmount": Number(expense.item.price),
                    "color": expense.category.color
                }
            }
            else {
                expense_data[expense.category.initial].totalAmount += Number(expense.item.price)
            }
        })
    })

    var sorted_expense_data = Object.entries(expense_data)
        .sort()
        .sort(([,e1], [,e2]) => e2.totalAmount-e1.totalAmount)
        .reduce((r, [k, v]) => ({...r, [k]: v}), {})

    return sorted_expense_data
}

const editExpense = async (expense_id) => {
    const expenseContainer = [...document.querySelectorAll('#expense')]
        .find((expense) => expense.dataset["expense_id"] === expense_id)


    const editFormPresent = expenseContainer.querySelector('#edit-expense-form')
    
    if (editFormPresent) {
        expenseContainer.removeChild(editFormPresent)
    }
    else {
        expenseContainer.appendChild(await createEditForm())
    }
}

const createEditForm = async () => {
    editForm = document.createElement('form')
    //create a form here. initally hidden, and have it animated when on editExpense
    editForm.id = "edit-expense-form"
    editForm.className = "form-group"

    itemName = document.createElement('input')
    itemName.className = "form-control"
    itemName.id = "newName"
    itemName.name = "name"
    itemName.placeholder = "Item Name"
    
    itemPrice = document.createElement('input')
    itemPrice.className = "form-control"
    itemPrice.name = "price"
    itemPrice.placeholder = "Item Price"
    itemPrice.type = "number"
    itemPrice.step = "0.01"

    itemDate = document.createElement('input')
    itemDate.className = "form-control"
    itemDate.name = "date"
    itemDate.type = "date"
    
    itemCategory = document.createElement('select')
    itemCategory.className = "form-control"
    itemCategory.name = "category"

    blankOption = document.createElement('option')
    blankOption.value = ""
    blankOption.disabled = true
    blankOption.selected = true
    blankOption.hidden = true
    blankOption.innerHTML = "Choose a Category"
    itemCategory.append(blankOption)

    const categories = await getCategories()
    categories.forEach(category => {
        newOption = document.createElement('option')
        newOption.innerHTML = category

        itemCategory.append(newOption)
    })

    itemDesc = document.createElement('input')
    itemDesc.className = "form-control"
    itemDesc.name = "desc"
    itemDesc.placeholder = "Description (optional)"

    itemLoc = document.createElement('input')
    itemLoc.className = "form-control"
    itemLoc.name = "loc"
    itemLoc.placeholder = "Location (optional)"

    submitEdit = document.createElement('input')
    submitEdit.className = "form-control"
    submitEdit.id = "edit-expense-submit"
    submitEdit.type = "button"
    submitEdit.value = "Update"

    editForm.append(itemName)
    editForm.append(itemPrice)
    editForm.append(itemDate)
    editForm.append(itemCategory)
    editForm.append(itemDesc)
    editForm.append(itemLoc)
    editForm.append(submitEdit)

    return editForm
}


const update_edit_form = (expense_id, form) => {
    edit_body = {}

    Array.from(form.children).forEach(element => {
        if (element.name !== "" && element.value !== "") {
            edit_body[element.name] = element.value
        }
    })

    if (Object.keys(edit_body).length === 0) {
        return
    }

    fetch(`/update_expense/${expense_id}`, {
        method: "Put",
        body: JSON.stringify(edit_body)
    })
    .then(() => {   
        reload_chart()
        reload_expenses()
    })
}

const reload_expenses = () => {
    parent = document.querySelector('#expenses')

    while (parent.firstChild) {
        parent.removeChild(parent.firstChild)
    }
    load_expenses()
}