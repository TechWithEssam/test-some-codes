const blankFormEl = document.querySelector("#blank-form")
   const attachmentContainer = document.querySelector("#attachments")
   const addAttachmentBtn = document.querySelector("#add-attachment-btn")
   const managementFormInputEl = document.querySelector("#id_form-TOTAL_FORMS")
   addAttachmentBtn.addEventListener("click", handleAttachmentBtnClick)
    function cloneBlankForm(){
        if (blankFormEl) {
            const newBlankForm = blankFormEl.cloneNode(true)
            const totalFormValue = parseInt(managementFormInputEl.value)
            var formRegex = new RegExp(`__prefix__`, 'g');
            newBlankForm.innerHTML = newBlankForm.innerHTML.replace(formRegex, totalFormValue)
            managementFormInputEl.value = totalFormValue + 1
            newBlankForm.classList.add("attachment-form")
            newBlankForm.classList.remove("hidden")
            newBlankForm.removeAttribute("id")
            // console.log(newBlankForm)
            return newBlankForm
        }
    }

    function handleAttachmentBtnClick(event) {
        if (event){
            event.preventDefault()
        }
        const newForm = cloneBlankForm()
        attachmentContainer.appendChild(newForm)
    }