    document.getElementById("openSidebar").onclick = () => {
      document.getElementById("sidebar").classList.add("show");
    };
    document.getElementById("closeSidebar").onclick = () => {
      document.getElementById("sidebar").classList.remove("show");
    };

    // Theme toggle
    document.getElementById("themeToggle").onclick = () => {
      document.body.classList.toggle("dark");
    };


    function previewImages(event) {
      const preview = document.getElementById("preview");
      preview.innerHTML = "";
      const files = event.target.files;
      if(files) {
        [...files].forEach(file => {
          const reader = new FileReader();
          reader.onload = e => {
            const img = document.createElement("img");
            img.src = e.target.result;
            preview.appendChild(img);
          }
          reader.readAsDataURL(file);
        });
      }
    }