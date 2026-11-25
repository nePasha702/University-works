export default function render({ data, parentElement, setTriggerValue }) {
  const root = parentElement.querySelector("#screen-root");
  const previous = root.querySelector(".screen")?.dataset.page;
  const search = root.querySelector("[data-search]")?.value;
  const openDetails = [...root.querySelectorAll("details[open][data-keep]")].map(el => el.dataset.keep);
  let busy = false;

  root.dataset.revision = data.revision;
  if (root.markup !== data.markup) {
    root.innerHTML = data.markup;
    root.markup = data.markup;
    if (previous === root.querySelector(".screen")?.dataset.page) {
      for (const item of root.querySelectorAll("details[data-keep]")) {
        item.open ||= openDetails.includes(item.dataset.keep);
      }
      if (search) {
        root.querySelector("[data-search]").value = search;
        filterDirectory(search);
      }
    } else {
      document.querySelector('[data-testid="stMain"]')?.scrollTo(0, 0);
    }
    const reveal = root.querySelector("[data-reveal]");
    if (reveal && previous) {
      requestAnimationFrame(() => reveal.scrollIntoView({ block: "nearest" }));
    }
  }

  function filterDirectory(value) {
    const query = value.trim().toLocaleLowerCase("ru");
    let visible = false;
    for (const card of root.querySelectorAll("[data-employee]")) {
      card.hidden = !card.dataset.employee.toLocaleLowerCase("ru").includes(query);
      visible ||= !card.hidden;
    }
    root.querySelector("[data-search-empty]").hidden = visible;
  }

  function emit(name, target, values = {}) {
    if (busy) return;
    busy = true;
    setTriggerValue("event", { name, target, values, revision: data.revision });
  }

  function click(event) {
    const button = event.target.closest('button[type="button"][data-action]');
    if (button) emit(button.dataset.action, button.dataset.target);
  }

  function submit(event) {
    const form = event.target.closest("form[data-form]");
    if (!form) return;
    event.preventDefault();
    const button = event.submitter;
    emit(button?.dataset.action ?? form.dataset.form, form.dataset.target,
      Object.fromEntries(new FormData(form)));
  }

  function input(event) {
    const control = event.target;
    if (control.matches("[data-search]")) filterDirectory(control.value);
    if (control.matches("[data-hours]")) {
      const values = JSON.parse(control.dataset.hours);
      control.form.elements.hours.value = values[control.value];
    }
    if (control.matches('.date-control input[type="date"]')) {
      const text = control.previousElementSibling;
      text.value = control.value.split("-").reverse().join(".");
    } else if (control.matches('.date-control input[type="text"]')) {
      const match = control.value.match(/^(\d{2})\.(\d{2})\.(\d{4})$/);
      control.nextElementSibling.value = match ? `${match[3]}-${match[2]}-${match[1]}` : "";
    }
  }

  const clock = root.querySelector("[data-live-clock]");
  let timer;
  if (clock) {
    const format = new Intl.DateTimeFormat("ru-RU", {
      timeZone: "Europe/Minsk", hour: "2-digit", minute: "2-digit", hourCycle: "h23",
    });
    timer = setInterval(() => { clock.textContent = format.format(new Date()); }, 1000);
  }
  root.addEventListener("click", click);
  root.addEventListener("submit", submit);
  root.addEventListener("input", input);
  return () => {
    clearInterval(timer);
    root.removeEventListener("click", click);
    root.removeEventListener("submit", submit);
    root.removeEventListener("input", input);
  };
}
