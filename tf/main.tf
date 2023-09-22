provider "google" {
    credentials = file("C:\\Users\\matacza\\Desktop\\Projekty\\BeautyScraper\\secrets\\skincare-project.json")
    project = "skincare-project-399418"
    region = "us-central1"
}

resource "google_storage_bucket" "amatacz-skincare-project-bucket" {
    name = "amatacz-skincare-project-bucket"
    location = "EU"
}