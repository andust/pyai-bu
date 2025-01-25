import MainLayout from "@/app/_layout/MainLayout";
import { cookies } from "next/headers";
import { EstimationFeed } from "../_models/estimation-feed";
import { getEstimationFeeds } from "../_utils/fetch/estimation-feed";


export default async function FeedEstimation() {
    let estimationFeeds: EstimationFeed[] = [];
  
    try {
      const cookieStore = await cookies();
      const access = cookieStore.get("access")?.value ?? "";
      const res = await getEstimationFeeds(access);
      console.log(res);
      
      if (res.ok) {
        estimationFeeds = await res.json();
      }
    } catch (error) {
      console.log(error);
    }
    console.log(estimationFeeds);
    
  return (
    <MainLayout>
      Estimation feeds
    </MainLayout>
  );
}
