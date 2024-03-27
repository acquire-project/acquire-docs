window.addEventListener("DOMContentLoaded", function() {

  // ABS_BASE_URL is the full URL
  // e.g. https://acquire-project.github.io/acquire-docs/dev/get_started/
  var ABS_BASE_URL = document.baseURI;
  // This should probably not be hardcoded
  var CURRENT_VERSION = ABS_BASE_URL.split("/")[4];
  var DOC_PATH = ABS_BASE_URL.split("/").slice(5).join("/")
  var root = ABS_BASE_URL.substring(0, ABS_BASE_URL.indexOf(CURRENT_VERSION));

  // Create dropdown menu
  function makeSelect(options) {
    var select = document.createElement("select");
    select.classList.add("form-control");

    options.forEach(function(i) {
      var option = new Option(i.text, i.value, undefined,
                              i.selected);
      select.add(option);
    });

    return select;
  }

  fetch(root+"versions.json").then((response) => {
    return response.json();
  }).then((versions) => {
    var realVersion = versions.find(function(i) {
      return i.version === CURRENT_VERSION ||
             i.aliases.includes(CURRENT_VERSION);
    }).version;

    var select = makeSelect(versions.filter(function(i) {
      return i.version === realVersion || !i.properties || !i.properties.hidden;
    }).map(function(i) {
      return {text: i.title, value: i.version,
              selected: i.version === realVersion};
    }));
    // Redirect to current page at selected version)
    select.addEventListener("change", function(event) {
      window.location.href = root + this.value + "/" + DOC_PATH;
    });

    var container = document.getElementById("version-selector");
    container.appendChild(select)
    var title = document.getElementById("site-title");
    if (title.parentNode.classList.contains("md-header__title")) {
      var height = window.getComputedStyle(title).getPropertyValue("height");
      container.style.height = height;
    }

    title.parentNode.insertBefore(container, title.nextElementSibling);
  });
});
