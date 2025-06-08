document.addEventListener("DOMContentLoaded", () => {
  // Fade out messages after 5 seconds
  const messages = document.querySelectorAll(".message")
  if (messages.length > 0) {
    setTimeout(() => {
      messages.forEach((message) => {
        message.style.transition = "opacity 0.5s ease"
        message.style.opacity = "0"

        setTimeout(() => {
          message.style.display = "none"
        }, 500)
      })
    }, 5000)
  }

  // Mobile menu toggle
  const mobileMenuToggle = document.querySelector(".mobile-menu-toggle")
  const nav = document.querySelector("nav")

  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener("click", () => {
      nav.classList.toggle("active")
    })
  }

  // Image preview for recipe form
  const imageInput = document.querySelector('input[type="file"]')
  if (imageInput) {
    imageInput.addEventListener("change", function () {
      const file = this.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          const previewContainer = document.querySelector(".current-image") || document.createElement("div")
          previewContainer.className = "current-image"

          if (!document.querySelector(".current-image")) {
            imageInput.parentNode.insertBefore(previewContainer, imageInput)
          }

          previewContainer.innerHTML = `
                        <img src="${e.target.result}" alt="Preview" width="150">
                        <p>Selected image: ${file.name}</p>
                    `
        }
        reader.readAsDataURL(file)
      }
    })
  }

  // User dropdown menu for mobile
  const userToggle = document.querySelector(".user-toggle")
  if (userToggle && window.innerWidth <= 768) {
    userToggle.addEventListener("click", function (e) {
      e.preventDefault()
      const dropdownMenu = this.nextElementSibling
      dropdownMenu.style.display = dropdownMenu.style.display === "block" ? "none" : "block"
    })
  }
})

