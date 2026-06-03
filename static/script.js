document.addEventListener("DOMContentLoaded", async () => {
    const hamburger = document.getElementById("hamburger");
    const navLinks = document.getElementById("nav-links");
    if (hamburger && navLinks) {
        hamburger.addEventListener("click", () => {
            navLinks.classList.toggle("open");
        });
    }


    const flashContainer = document.getElementById("flash-container");

    if (flashContainer) {
        setTimeout(() => {
            flashContainer.style.display = "none";
        }, 3000);
    }

    async function loadCatalog() {
        const response = await fetch("/api/catalog");
        const catalog = await response.json();
        return catalog
    }

    const selectedServiceDisplay = document.getElementById("selected-service-display");
    const userBookingServicesModal = document.getElementById("user-booking-services-modal");

    if (selectedServiceDisplay && userBookingServicesModal) {

        const catalog = await loadCatalog();
        const selectedServices = new Set(
            selectedServiceDisplay.value
                .split(",")
                .map(service => service.trim())
                .filter(Boolean)
        );

        const updateSelectedServiceDisplay = () => {
            selectedServiceDisplay.value = Array.from(selectedServices).join(", ");
        };

        const escapeHtml = (value) => String(value ?? "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");

        const renderServicesModal = () => {
            userBookingServicesModal.innerHTML = `
                <h2>Select Services</h2>
                <div id="selected-services">
                    ${catalog.map(service => {
                        const serviceName = String(service.name ?? "");
                        const escapedName = escapeHtml(serviceName);
                        return `
                            <label class="card" for="service-${service.id}">
                                <input type="checkbox" id="service-${service.id}" value="${escapeHtml(service.id)}" data-service-name="${escapedName}" ${selectedServices.has(serviceName) ? "checked" : ""}>
                                <h3>${escapedName}</h3>
                                <p>${escapeHtml(service.description)}</p>
                            </label>
                        `;
                    }).join("")}
                </div>
                <button id="user-booking-services-modal-close" type="button">Close</button>
            `;
        };

        selectedServiceDisplay.addEventListener("click", () => {
            renderServicesModal();
            userBookingServicesModal.showModal();
        });

        userBookingServicesModal.addEventListener("change", (event) => {
            if (!event.target.matches("#selected-services input[type='checkbox']")) {
                return;
            }

            const serviceName = event.target.dataset.serviceName;
            if (event.target.checked) {
                selectedServices.add(serviceName);
            } else {
                selectedServices.delete(serviceName);
            }

            updateSelectedServiceDisplay();
        });

        userBookingServicesModal.addEventListener("click", (event) => {
            if (event.target.id === "user-booking-services-modal-close") {
                userBookingServicesModal.close();
            }
        });

    }

    const bookingForm = document.getElementById("booking-request-form");
    const bookingDate = document.getElementById("date");
    const bookingTime = document.getElementById("time");
    const bookingSubmit = document.getElementById("booking-submit");
    const availabilityStatus = document.getElementById("availability-status");

    if (bookingForm && bookingDate && bookingTime && bookingSubmit && availabilityStatus) {
        const setAvailabilityStatus = (message, state) => {
            availabilityStatus.textContent = message;
            availabilityStatus.dataset.state = state;
            bookingSubmit.disabled = state === "unavailable" || state === "checking";
        };

        const checkAvailability = async () => {
            if (!bookingDate.value || !bookingTime.value) {
                setAvailabilityStatus("", "idle");
                bookingSubmit.disabled = false;
                return;
            }

            setAvailabilityStatus("Checking availability...", "checking");

            try {
                const params = new URLSearchParams({
                    date: bookingDate.value,
                    time: bookingTime.value,
                });
                const response = await fetch(`/api/availability?${params}`, {
                    headers: { "Accept": "application/json" },
                });

                if (!response.ok) {
                    throw new Error("Availability request failed");
                }

                const result = await response.json();
                if (result.available) {
                    setAvailabilityStatus("This time is available.", "available");
                } else {
                    setAvailabilityStatus("That time is already booked. Please choose another time.", "unavailable");
                }
            } catch (error) {
                setAvailabilityStatus("Availability could not be checked. You can still submit and we will verify it.", "unknown");
                bookingSubmit.disabled = false;
            }
        };

        bookingDate.addEventListener("change", checkAvailability);
        bookingTime.addEventListener("change", checkAvailability);
    }


    const itemCard = document.querySelectorAll(".admin-item-card");
    const itemCardModal = document.getElementById("admin-item-card-modal");
    const itemImageModal = document.getElementById("admin-item-image-modal");
    const itemCategoryModal = document.getElementById("admin-item-category-modal");
    const itemNameModal = document.getElementById("admin-item-name-modal");
    const itemPriceModal = document.getElementById("admin-item-price-modal");
    const itemDescriptionModal = document.getElementById("admin-item-description-modal");
    const itemCloseButton = document.getElementById("admin-item-close-modal");

    if (itemCard.length && itemCardModal && itemImageModal && itemCategoryModal && itemNameModal && itemPriceModal && itemDescriptionModal && itemCloseButton) {
        itemCard.forEach(card => {
            card.addEventListener("click", (event) => {
                event.stopPropagation();
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

    if (userItemCard.length && userCardModal && userCardImageModal && userCardCategoryModal && userCardNameModal && userCardPriceModal && userCardDescriptionModal && userCardCloseButton) {
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

    if (
        userFilteredCatalogCard.length &&
        userFilteredCatalogModal &&
        userFilteredCatalogImageModal &&
        userFilteredCatalogNameModal &&
        userFilteredCatalogCategoryModal &&
        userFilteredCatalogDescriptionModal &&
        userFilteredCatalogPriceModal &&
        userFilteredCatalogCloseButton
    ) {
        userFilteredCatalogCard.forEach(card => {
            card.addEventListener("click", () => {
                userFilteredCatalogImageModal.src = "/static/" + card.dataset.image;
                userFilteredCatalogNameModal.textContent = card.dataset.name;
                userFilteredCatalogCategoryModal.textContent = `Category: ${card.dataset.category}`;
                userFilteredCatalogDescriptionModal.textContent = `Description: ${card.dataset.description}`;
                userFilteredCatalogPriceModal.textContent = `Price: R${card.dataset.price}`;
                userFilteredCatalogModal.showModal();
            });
        });

        userFilteredCatalogCloseButton.addEventListener("click", () => {
            userFilteredCatalogModal.close();
        });
    }
    

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
                bookingRequestConfirmMessageModal.textContent = `Accept Booking for ${confirmButton.closest(".booking-request-card").dataset.name}?`;
                
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
    const bookingRequestDeclinkLink = document.getElementById("booking-request-decline-link");

    if (bookingRequestReject.length && bookingRequestRejectModal && bookingRequestRejectMessageModal && bookingRequestRejectCancelButton && bookingRequestDeclinkLink) {
        bookingRequestReject.forEach(rejectButton => {
            rejectButton.addEventListener("click", (event) => {
                event.stopPropagation();
                bookingRequestRejectMessageModal.textContent = `Reject Booking for ${rejectButton.closest(".booking-request-card").dataset.name}?`;

                const request_id = rejectButton.closest(".booking-request-card").dataset.request_id;
                bookingRequestDeclinkLink.href = `/admin_booking_requests/decline/${request_id}`;

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
    const appointmentCompleteButtons = document.querySelectorAll(".appointment-complete");
    const appointmentCancelButtons = document.querySelectorAll(".appointment-cancel");
    const appointmentStatusCompletedModal = document.getElementById("appointment-status-completed-modal");
    const appointmentStatusCancelledModal = document.getElementById("appointment-status-cancelled-modal");
    const appointmentStatusCompletedMessageModal = document.getElementById("appointment-status-completed-message-modal");
    const appointmentStatusCancelledMessageModal = document.getElementById("appointment-status-cancelled-message-modal");
    const appointmentCompleteLink = document.getElementById("appointment-complete-link");
    const appointmentCancelLink = document.getElementById("appointment-cancel-link");
    const appointmentCompleteCancelModal = document.getElementById("appointment-complete-cancel-modal");
    const appointmentCancelCancelModal = document.getElementById("appointment-cancel-cancel-modal");

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

    if (appointmentCompleteButtons.length && appointmentStatusCompletedModal && appointmentStatusCompletedMessageModal && appointmentCompleteLink && appointmentCompleteCancelModal) {
        appointmentCompleteButtons.forEach(button => {
            button.addEventListener("click", (event) => {
                event.stopPropagation();
                const card = button.closest(".appointment-card");
                const appointmentId = card.dataset.appointmentId;
                appointmentStatusCompletedMessageModal.textContent = `Mark appointment for ${card.dataset.name} as completed?`;
                appointmentCompleteLink.href = `/admin_appointments/complete/${appointmentId}`;
                appointmentStatusCompletedModal.showModal();
            });
        });

        appointmentCompleteCancelModal.addEventListener("click", () => {
            appointmentStatusCompletedModal.close();
        });
    }

    if (appointmentCancelButtons.length && appointmentStatusCancelledModal && appointmentStatusCancelledMessageModal && appointmentCancelLink && appointmentCancelCancelModal) {
        appointmentCancelButtons.forEach(button => {
            button.addEventListener("click", (event) => {
                event.stopPropagation();
                const card = button.closest(".appointment-card");
                const appointmentId = card.dataset.appointmentId;
                appointmentStatusCancelledMessageModal.textContent = `Cancel appointment for ${card.dataset.name}?`;
                appointmentCancelLink.href = `/admin_appointments/cancel/${appointmentId}`;
                appointmentStatusCancelledModal.showModal();
            });
        });

        appointmentCancelCancelModal.addEventListener("click", () => {
            appointmentStatusCancelledModal.close();
        });
    }
});


