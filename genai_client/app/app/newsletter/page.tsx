import MainLayout from "@/app/_layout/MainLayout";
import NewsletterGeneratorForm from "../_molecules/newsletter-generator-form/NewsletterGeneratorForm";

export default async function New() {
  
  return (
    <MainLayout>
      Newsletter generator
      <NewsletterGeneratorForm />
    </MainLayout>
  );
}
