import MainLayout from "@/app/_layout/MainLayout";
import ScrapePageForm from "../_molecules/scrap-page-form/ScrapPageForm";

export default async function New() {
  
  return (
    <MainLayout>
      Scraper
      <ScrapePageForm />
    </MainLayout>
  );
}
