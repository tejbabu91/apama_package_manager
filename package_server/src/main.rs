use actix_web::{web, App, HttpRequest, HttpResponse, HttpServer, Responder};
use serde::Deserialize;

#[derive(Deserialize, Debug)]
struct PackageQuery {
    name: String,
}

fn listpackages(req: HttpRequest, q: web::Query<PackageQuery>) -> impl Responder {
    // let name: String = req.match_info().query("name").parse().unwrap();
    format!("Name: {:?}", q)
}

fn main() {
    HttpServer::new(|| App::new().route("/listpackages", web::get().to(listpackages)))
        .bind("0.0.0.0:8000")
        .expect("bind to port failed")
        .run()
        .unwrap();
}
