import { useEffect } from "react";
import { useParams } from "react-router-dom";

const DetailPage = () => {
  const param = useParams();
  useEffect(() => {
    console.log("param->", param);
  }, [param]);

  return <>DetailPage</>;
};

export default DetailPage;
