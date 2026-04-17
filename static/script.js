document.addEventListener("DOMContentLoaded", () => {
    const hamburger = document.getElementById("hamburger");
    const navLinks = document.getElementById("nav-links");
    hamburger.addEventListener("click", () => {
        navLinks.classList.toggle("open");
    });


    const flashContainer = document.getElementById("flash-container");

    if (flashContainer) {
    setTimeout(() => {
        flashContainer.style.display = "none";
    }, 3000);
    }


    const itemCard = document.querySelectorAll(".admin-item-card");
    const itemCardModal = document.getElementById("admin-item-card-modal");
    const itemImageModal = document.getElementById("admin-item-image-modal")
    const itemCategoryModal = document.getElementById("admin-item-category-modal");
    const itemNameModal = document.getElementById("admin-item-name-modal");
    const itemPriceModal = document.getElementById("admin-item-price-modal");
    const itemDescriptionModal = document.getElementById("admin-item-description-modal");
    const itemCloseButton = document.getElementById("admin-item-close-modal");

    if (itemCard.length && itemCardModal && itemCategoryModal && itemNameModal && itemPriceModal && itemDescriptionModal && itemCloseButton) {
        itemCard.forEach(card => {
            card.addEventListener("click", () => {
                itemImageModal.src = "/static/" + card.dataset.image;
                itemCategoryModal.textContent = `Category: ${card.dataset.category}`;
                itemNameModal.textContent = `Name: ${card.dataset.name}`;
                itemPriceModal.textContent = `Price: R${card.dataset.price}`;
                itemDescriptionModal.innerHTML = `Description:</br>${card.dataset.description}`;
                itemCardModal.showModal();
            });
        });

        itemCloseButton.addEventListener("click", () => {
            itemCardModal.close();
        });
    }

    const exitPrompt = document.getElementById("exit-prompt");
    const exitModal = document.getElementById("exit-modal");
    const exitCancelModal = document.getElementById("exit-cancel-modal");

    if (exitPrompt && exitModal && exitCancelModal) {
        exitPrompt.addEventListener("click", () => {
            exitModal.showModal();
        });

        exitCancelModal.addEventListener("click", () => {
            exitModal.close();
        });
    }


    const userItemCard = document.querySelectorAll(".user-item-card, .user-catalog-item-card");
    const userCardModal = document.getElementById("user-item-card-modal");
    const userCardCategoryModal = document.getElementById("user-item-category-modal");
    const userCardNameModal = document.getElementById("user-item-name-modal");
    const userCardPriceModal = document.getElementById("user-item-price-modal");
    const userCardDescriptionModal = document.getElementById("user-item-description-modal");
    const userCardCloseButton = document.getElementById("user-item-close-modal");
    const userCardImageModal = document.getElementById("user-item-image-modal");

    if (userItemCard.length && userCardModal && userCardCategoryModal && userCardNameModal && userCardPriceModal && userCardDescriptionModal && userCardCloseButton) {
        userItemCard.forEach(card => {
            card.addEventListener("click", () => {
                userCardImageModal.src = "/static/" + card.dataset.image;
                userCardCategoryModal.textContent = `Category: ${card.dataset.category}`;
                userCardNameModal.textContent = card.dataset.name;
                userCardPriceModal.textContent = `Price: R${card.dataset.price}`;
                userCardDescriptionModal.textContent = `Description: ${card.dataset.description}`;
                userCardModal.showModal();
            });
        });

        userCardCloseButton.addEventListener("click", () => {
            userCardModal.close();
        });
    }


    const userFilteredCatalogCard = document.querySelectorAll(".user-filtered-catalog-card");
    const userFilteredCatalogModal = document.getElementById("user-filtered-catalog-modal");
    const userFilteredCatalogImageModal = document.getElementById("user-filtered-catalog-image-modal");
    const userFilteredCatalogNameModal = document.getElementById("user-filtered-catalog-name-modal");
    const userFilteredCatalogCategoryModal = document.getElementById("user-filtered-catalog-category-modal");
    const userFilteredCatalogDescriptionModal = document.getElementById("user-filtered-catalog-description-modal");
    const userFilteredCatalogPriceModal = document.getElementById("user-filtered-catalog-price-modal");
    const userFilteredCatalogCloseButton = document.getElementById("user-filter-catalog-close-modal");

    userFilteredCatalogCard.forEach(card => {
        card.addEventListener("click", () => {
            userFilteredCatalogImageModal.src ="/static/" + card.dataset.image;
            userFilteredCatalogModal.showModal();
        });
    });

    userFilteredCatalogCloseButton.addEventListener("click", () => {
        userFilteredCatalogModal.close();
    });
    

    const bookingRequestCard = document.querySelectorAll(".booking-request-card");
    const bookingRequestCardModal = document.getElementById("booking-request-card-modal");
    const bookingRequestSelectedServiceModal = document.getElementById("booking-request-selected-service-modal");
    const bookingRequestNameModal = document.getElementById("booking-request-name-modal");
    const bookingRequestPhoneModal = document.getElementById("booking-request-phone-modal");
    const bookingRequestEmailModal = document.getElementById("booking-request-email-modal");
    const bookingRequestMessageModal = document.getElementById("booking-request-message-modal");
    const bookingRequestCardModalClose = document.getElementById("booking-request-card-modal-close");

    if (bookingRequestCard.length && bookingRequestCardModal && bookingRequestSelectedServiceModal && bookingRequestNameModal && bookingRequestPhoneModal && bookingRequestEmailModal && bookingRequestMessageModal && bookingRequestCardModalClose) {
        bookingRequestCard.forEach(card => {
            card.addEventListener("click", () => {
                bookingRequestSelectedServiceModal.textContent = card.dataset.selected_service;
                bookingRequestNameModal.textContent = card.dataset.name;
                bookingRequestPhoneModal.textContent = card.dataset.phone;
                bookingRequestEmailModal.textContent = card.dataset.email;
                bookingRequestMessageModal.textContent = card.dataset.message;
                bookingRequestCardModal.showModal();
            });
        });

        bookingRequestCardModalClose.addEventListener("click", () => {
            bookingRequestCardModal.close();
        });
    }


    const bookingRequestConfirmLink = document.getElementById("booking-request-confirm-link");
    const bookingRequestAccept = document.querySelectorAll(".booking-request-accept");
    const bookingRequestConfirmModal = document.getElementById("booking-request-confirm-modal");
    const bookingRequestConfirmMessageModal = document.getElementById("booking-request-confirm-message-modal");
    const bookingRequestConfirmCancelButton = document.getElementById("booking-request-confirm-cancel-button");

    if (bookingRequestAccept.length && bookingRequestConfirmLink && bookingRequestConfirmModal && bookingRequestConfirmMessageModal && bookingRequestConfirmCancelButton) {
        bookingRequestAccept.forEach(confirmButton => {
            confirmButton.addEventListener("click", (event) => {
                event.stopPropagation();
                bookingRequestConfirmMessageModal.textContent = `Accept Booking for ${confirmButton.closest(".booking-request-card").dataset.name}?`
                
                const request_id = confirmButton.closest(".booking-request-card").dataset.request_id;
                bookingRequestConfirmLink.href = `/admin_booking_requests/accept/${request_id}`;

                bookingRequestConfirmModal.showModal();
    
            });
        });

        bookingRequestConfirmCancelButton.addEventListener("click", () => {
            bookingRequestConfirmModal.close();
        });
    }



    const bookingRequestReject = document.querySelectorAll(".booking-request-reject");
    const bookingRequestRejectModal = document.getElementById("booking-request-reject-modal");
    const bookingRequestRejectMessageModal = document.getElementById("booking-request-reject-message-modal");
    const bookingRequestRejectCancelButton = document.getElementById("booking-request-reject-cancel-button");
    const bookingRequestDeclinkLink = document.getElementById("booking-request-decline-link")

    if (bookingRequestReject.length && bookingRequestRejectModal && bookingRequestRejectMessageModal && bookingRequestRejectCancelButton && bookingRequestDeclinkLink) {
        bookingRequestReject.forEach(rejectButton => {
            rejectButton.addEventListener("click", (event) => {
                event.stopPropagation();
                bookingRequestRejectMessageModal.textContent = `Reject Booking for ${rejectButton.closest(".booking-request-card").dataset.name}?`

                const request_id = rejectButton.closest(".booking-request-card").dataset.request_id;
                bookingRequestDeclinkLink.href = `admin_booking_requests/decline/${request_id}`;

                bookingRequestRejectModal.showModal();
            });
        });

        bookingRequestRejectCancelButton.addEventListener("click", () => {
            bookingRequestRejectModal.close();
        });
    }


    const appointmentCard = document.querySelectorAll(".appointment-card");
    const appointmentModal = document.getElementById("appointment-modal");
    const appointmentIdModal = document.getElementById("appointment-id-modal");
    const appointmentServiceModal = document.getElementById("appointment-service-modal");
    const appointmentNameModal = document.getElementById("appointment-name-modal");
    const appointmentEmailModal = document.getElementById("appointment-email-modal");
    const appointmentPhoneModal = document.getElementById("appointment-phone-modal");
    const appointmentDateTimeModal = document.getElementById("appointment-date-time-modal");
    const appointmentMessageModal = document.getElementById("appointment-message-modal");
    const appointmentCloseModal = document.getElementById("appointment-close-modal");

    if (appointmentCard.length && appointmentModal && appointmentIdModal && appointmentServiceModal && appointmentNameModal && appointmentEmailModal && appointmentPhoneModal && appointmentDateTimeModal && appointmentMessageModal && appointmentCloseModal) {
        appointmentCard.forEach(card => {
            card.addEventListener("click", () => {
                appointmentIdModal.textContent = `Appointment ID: ${card.dataset.appointmentId }`;
                appointmentServiceModal.textContent = `Service: ${card.dataset.service}`;
                appointmentNameModal.textContent = `Name: ${card.dataset.name}`;
                appointmentEmailModal.textContent = `Email: ${card.dataset.email}`;
                appointmentPhoneModal.textContent = `Phone: ${card.dataset.phone}`;
                appointmentDateTimeModal.textContent = `Date & Time: ${card.dataset.date} ${card.dataset.time || ""}`.trim();
                appointmentMessageModal.textContent = `Message: ${card.dataset.message}`;
                appointmentModal.showModal();
            });
        });

        appointmentCloseModal.addEventListener("click", () => {
            appointmentModal.close();
        });
    }
});



