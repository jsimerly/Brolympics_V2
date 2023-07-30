import {useState} from 'react'
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import AssignmentTurnedInOutlinedIcon from '@mui/icons-material/AssignmentTurnedInOutlined';

const CopyWrapper = ({copyString, size, children}) => {
const [copySuccess, setCopySuccess] = useState(false);
const copyToClipboard = async () => {
    if (!navigator.clipboard) {
        // Clipboard API not available
        return;
    }
    try {
        await navigator.clipboard.writeText(copyString);
        setCopySuccess(true);
        setTimeout(() => {
        setCopySuccess(false);
        }, 3000);
    } catch (err) {
        console.log('Could not copy.')
    }
    }
    
  return (
    <div
      onClick={copyToClipboard}
      className='flex w-full h-full'
    >
      {children}
      {copySuccess ?
        <AssignmentTurnedInOutlinedIcon 
          sx={{fontSize:size}}
        /> 
        :
        <ContentCopyIcon 
          sx={{fontSize:size}}
        />
      }
    </div>
  )
}

export default CopyWrapper