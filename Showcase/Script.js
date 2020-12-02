function fillElements() {
  var Section = document.getElementById("ItemSpace");
  var NewsData = MyData;
  var GenreList = Object.keys(NewsData[0]);

  for (var Genre = 0; Genre < GenreList.length; Genre++) {
    
    var GenreSpace = document.createElement("tr");
    GenreSpace.className
    Section.append(GenreSpace);
    var GenreCont = document.createElement("td");
    GenreSpace.append(GenreCont);
    GenreCont.className = "GenreCont";

    var GenreTable = document.createElement("table");
    GenreTable.className = "GenreTable";
    GenreCont.append(GenreTable);

    var HeadRow = document.createElement("tr");
    GenreTable.append(HeadRow);
    HeadRow.className = "HeadRow";
    var GenreHead = document.createElement("th");
    GenreHead.className = "GenreHead";
    HeadRow.append(GenreHead);
    var GenreData = GenreList[Genre];
    GenreHead.innerHTML = GenreData.toUpperCase();

    for (var Cluster = 0; Cluster < NewsData[0][GenreList[Genre]].length; Cluster++) {
      var Row = document.createElement("tr");
      Row.className = "ClusterRow"
      GenreTable.appendChild(Row);

      var NewsCluster = document.createElement("div");
      NewsCluster.className = "NewsCluster";
      Row.appendChild(NewsCluster);

      var ImageCol = document.createElement("td");
      NewsCluster.appendChild(ImageCol);
      ImageCol.className = "ItemCol ImageCol";

      var Image = document.createElement("img");
      ImageCol.appendChild(Image);
      Image.className = "NewsThumbs";
      Image.src = NewsData[0][GenreList[Genre]][Cluster][0].imageLink;

      var NewsCol = document.createElement("td");
      NewsCluster.appendChild(NewsCol);
      NewsCol.className = "ItemCol HeadCol";

      var ClusterTab = document.createElement("table");
      NewsCol.appendChild(ClusterTab);
      ClusterTab.className = "ClusterTab";

      for(var NewsItem = 0; NewsItem < NewsData[0][GenreList[Genre]][Cluster].length; NewsItem++){
        var HeadTabRow = document.createElement("tr");
        ClusterTab.appendChild(HeadTabRow);
        var HeadListItem = "";
        var SrcItem = "";
        if(NewsItem === 0){
          HeadListItem = document.createElement("th");
          SrcItem = document.createElement("th");
        }
        else{
          HeadListItem = document.createElement("td");
          SrcItem = document.createElement("td");
        }
        HeadListItem.className = "HeadListItem";
        SrcItem.className = "SrcItem";
        HeadTabRow.appendChild(HeadListItem);
        HeadTabRow.appendChild(SrcItem);

        var HeadLine = document.createElement("a");
        HeadListItem.appendChild(HeadLine);
        HeadLine.className = "HeadLine";
        HeadLine.href = NewsData[0][GenreList[Genre]][Cluster][NewsItem].storyLink;
        HeadLine.innerHTML = NewsData[0][GenreList[Genre]][Cluster][NewsItem].headLine;

        var Source = document.createElement("a");
        SrcItem.appendChild(Source)
        Source.className = "Source";
        Source.href = NewsData[0][GenreList[Genre]][Cluster][NewsItem].sourceLink;
        Source.innerHTML = NewsData[0][GenreList[Genre]][Cluster][NewsItem].Source;
      }
    }
  }
}
