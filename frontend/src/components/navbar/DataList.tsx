const DataList = ({title, data, card}) => {
    return (
        <div className="">
            <h2 className="text-[20px]">
                {title}
            </h2>
            <div>
                {data.length === 0 ? 
                    `No ${title}`
                    :
                    data.map(card)
                }
            </div>
        </div>
    );
}

export default DataList;
