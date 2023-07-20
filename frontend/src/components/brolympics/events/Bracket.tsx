import BracketNode from "./BracketNode"
import { TeamNode } from "./BracketNode"

const BracketConnection = ({}) => (
    <div className="flex items-center">
        <div className="inline-flex flex-col gap-6">
            <BracketNode/>
            <BracketNode/>
        </div>  
        <div className="w-[2px] bg-primary h-[110px]"/>
        <div className="h-[2px] bg-primary w-[16px] mr-3"/>
    </div>
)

const Bracket = () => {
  return (
    <div className="px-6 pb-6 overflow-auto">
        <h4 className="text-[12px] pb-2">Winners</h4>
        <div className="flex items-center w-[720px]">
            <BracketConnection/>
            <BracketNode/>
            <div className="pr-3"/>
            <TeamNode/>
        </div>
        <h4 className="text-[12px] pb-2 pt-3">
            Losers
        </h4>
        <div className="flex items-center ">
            <BracketNode/>
            <div className="pr-3"/>
            <TeamNode/>
        </div>
    </div>
  )
}

export default Bracket