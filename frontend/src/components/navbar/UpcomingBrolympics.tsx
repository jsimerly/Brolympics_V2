
import DataList from './DataList';

const UpcomingBrolympics = ({upcoming_brolympics}) => {
    const Card = (info, index) => (
        <div className='flex items-center w-full gap-3 p-3 rounded-md fex-items-center' key={index}> 
            <div className='bg-white h-[40px] w-[40px] rounded-lg text-black'>
                logo
            </div>
            <div className="flex flex-col">
                <h3 className="text-[18px]">{info.name}</h3>
                <div className='text-[14px] ml-1 opacity-60'>
                {info.projected_start_date} - {info.projected_end_date}
                </div>
            </div>
        </div>
    );

    return (
        <DataList
            title="Upcoming Brolympics"
            data={upcoming_brolympics}
            card={Card}
        />
    )
}

export default UpcomingBrolympics;