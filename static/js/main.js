const form = document.querySelector("#lead-form");
const submitButton = form?.querySelector(".submit-button");
const statusMessage = form?.querySelector(".form-status");

const validators = {
  fullName(value) {
    if (!value.trim()) return "Enter your full name.";
    if (value.trim().length < 2) return "Name must be at least 2 characters.";
    return "";
  },
  workEmail(value) {
    if (!value.trim()) return "Enter your work email.";
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim())) {
      return "Enter a valid work email address.";
    }
    return "";
  },
  companyName(value) {
    if (!value.trim()) return "Enter your company name.";
    if (value.trim().length < 2) return "Company name must be at least 2 characters.";
    return "";
  },
  companyWebsite(value) {
    if (!value.trim()) return "Enter your company website.";

    try {
      const url = new URL(value.trim());
      if (!["http:", "https:"].includes(url.protocol) || !url.hostname.includes(".")) {
        return "Enter a valid website URL.";
      }
    } catch {
      return "Include a valid URL, such as https://company.com.";
    }

    return "";
  },
  industry() {
    return "";
  },
};

function setFieldState(input, message) {
  const field = input.closest(".field");
  const error = document.querySelector(`#${input.id}-error`);

  field.classList.toggle("is-invalid", Boolean(message));
  field.classList.toggle("is-valid", !message && Boolean(input.value.trim()));

  input.setAttribute("aria-invalid", String(Boolean(message)));
  if (message) {
    input.setAttribute("aria-describedby", `${input.id}-error`);
  } else {
    input.removeAttribute("aria-describedby");
  }

  if (error) {
    error.textContent = message;
  }
}

function validateInput(input) {
  const validate = validators[input.name];
  const message = validate ? validate(input.value) : "";
  setFieldState(input, message);
  return !message;
}

function validateForm() {
  const inputs = Array.from(form.querySelectorAll("input"));
  return inputs.map(validateInput).every(Boolean);
}

function setLoading(isLoading) {
  submitButton.classList.toggle("is-loading", isLoading);
  submitButton.disabled = isLoading;
  submitButton.querySelector(".button-label").textContent = isLoading
    ? "Generating report..."
    : "Generate Personalized Report";
}

if (form) {
  form.querySelectorAll("input").forEach((input) => {
    input.addEventListener("blur", () => validateInput(input));
    input.addEventListener("input", () => {
      if (input.closest(".field").classList.contains("is-invalid")) {
        validateInput(input);
      }
    });
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    statusMessage.textContent = "";

    if (!validateForm()) {
      statusMessage.textContent = "Please fix the highlighted fields to continue.";
      statusMessage.style.color = "var(--danger)";
      form.querySelector(".is-invalid input")?.focus();
      return;
    }

    setLoading(true);
    form.submit();
  });
}
