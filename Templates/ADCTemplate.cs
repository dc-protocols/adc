using System;
using System.Net;
using System.Collections.Generic;

namespace ADC
{
    /// <summary>
    /// !(COMMAND_DESCRIPTION)
    /// </summary>
    public class !(COMMAND_NAME) : ADCCommand
    {
        #region Constants

        private const string COMMAND_NAME = "!(COMMAND_ID)";
        private const string SEPARATOR = " ";

        #endregion

        #region Enums

        /// START FOR EACH ENUMTYPE
        /// <summary>
        /// !(ENUM_DESCRIPTION)
        /// </summary>
        !(FLAGS_ATTRIBUTE)
        public enum !(ENUM_NAME)
        {
            /// <summary>
            /// Basic holder for unknown values
            /// </summary>
            Unknown = 0,

            /// START FOR EACH ENUM_VALUE
            /// <summary>
            /// !(ENUM_VALUE_DESCRIPTION)
            /// </summary>
            !(ENUM_VALUE_NAME) = !(ENUM_VALUE_VALUE)
            /// END FOR EACH ENUM_VALUE
        }
        /// END FOR EACH ENUMTYPE

        #endregion

        #region Positional parameters

        /// START FOR EACH POSITIONAL_PARAMETER
        /// <summary>
        /// !(PARAMETER_DESCRIPTION)
        /// </summary>
        public !(PARAMETER_TYPE) !(PARAMETER_NAME)
        {
            get;
            set;
        }
        /// END FOR EACH POSITIONAL_PARAMETER
        
        #endregion

        #region Named parameters

        /// START FOR EACH NAMED_PARAMETER
        /// <summary>
        /// !(PARAMETER_DESCRIPTION)
        /// </summary>
        public !(PARAMETER_TYPE) !(PARAMETER_NAME)
        {
            get;
            set;
        }
        /// END FOR EACH NAMED_PARAMETER
        
        #endregion

        #region Constructors

        public !(COMMAND_NAME)()
        {
        }

        #endregion

        #region Methods

        /// START FOR EACH POSITIONAL_PARAMETERS
        /// <summary>
        /// 
        /// </summary>
        public string Get!(PARAMETER_NAME)Value()
        {
            string message = !(REPLACE_VALUE);
            
            return message;
        }
        /// END FOR EACH POSITIONAL_PARAMETERS

        /// START FOR EACH NAMED_PARAMETERS
        /// <summary>
        /// 
        /// </summary>
        public string Get!(PARAMETER_NAME)Value()
        {
            string message = "!(PARAMETER_ID)" + !(REPLACE_VALUE);
            
            return message;
        }
        /// END FOR EACH NAMED_PARAMETERS

        #endregion

        #region Base class overrides

        public override string CommandName
        {
            get { return "!(COMMAND_ID)"; }
        }

        /// <summary>
        /// 
        /// </summary>
        public override string ConstructMessage()
        {
            string message = "";

            // Positional parameters
            /// START FOR EACH POSITIONAL_PARAMETERS
            
            if (!(PARAMETER_NAME) == !(PARAMETER_NULL_VALUE))
            {
                throw new Exception("!(PARAMETER_NAME) cannot be !(PARAMETER_NULL_VALUE)!");
            }

            message += SEPARATOR;
            message += Get!(PARAMETER_NAME)Value();
            /// END FOR EACH POSITIONAL_PARAMETERS
            
            // Named parameters
            /// START FOR EACH NAMED_PARAMETERS
            
            if (!(PARAMETER_NAME) != !(PARAMETER_NULL_VALUE))
            {
                message += SEPARATOR;
                message += Get!(PARAMETER_NAME)Value();
            }
            /// END FOR EACH NAMED_PARAMETERS

            message = message.Substring(1);
            return message; 
        }

        #endregion
    }
}